# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import math
# from itertools import chain

import bpy
from bpy.props import *
import blf
# import mathutils as Math
from mathutils import Euler, Vector, Quaternion, Matrix
import bgl


"""
RegionView3D.view_matrix == modelview_matrix
RegionView3D.perspective_matrix == projection_matrix * modelview_matrix
persmat = winmat * viewmat
"""


GLA_PIXEL_OFS = 0.375

class Buffer:
    def __new__(self, type, dimensions=0, template=None):
        """
        :param type: GL_BYTE('bool','byte'), GL_SHORT('short'),
            GL_INT('int'), GL_FLOAT('float') or GL_DOUBLE('double')
        :type type: int | str
        :param dimensions: array size.
            e.g. 3:      [0, 0, 0]
                 [4, 2]: [(0, 0), (0, 0), (0, 0), (0, 0)]
        :type dimensions: int | list | tuple
        :param template: Used to initialize the Buffer
            e.g. list: [1, 2, 3], int: bgl.GL_BLEND
        :type template: None | sequence | int
        :return:
        :rtype:
        """
        if isinstance(type, str):
            type = type.lower()
            if type in ('bool', 'byte'):
                type = bgl.GL_BYTE
            elif type == 'short':
                type = bgl.GL_SHORT
            elif type == 'int':
                type = bgl.GL_INT
            elif type == 'float':
                type = bgl.GL_FLOAT
            elif type == 'double':
                type = bgl.GL_DOUBLE
            else:
                type = None

        return_int = isinstance(dimensions, int) and dimensions < 1
        if return_int:
            dim = 1
        else:
            dim = dimensions
        if template is None:
            buf = bgl.Buffer(type, dim)
        elif isinstance(template, int):
            if type == bgl.GL_BYTE:
                glGet = bgl.glGetBooleanv
            elif type == bgl.GL_SHORT:
                glGet = bgl.glGetIntegerv
            elif type == bgl.GL_INT:
                glGet = bgl.glGetIntegerv
            elif type == bgl.GL_FLOAT:
                glGet = bgl.glGetFloatv
            elif type == bgl.GL_DOUBLE:
                glGet = bgl.glGetDoublev
            else:
                msg = "invalid first argument type, should be one of " \
                      "GL_BYTE('bool','byte'), GL_SHORT('short'), " \
                      "GL_INT('int'), GL_FLOAT('float') or GL_DOUBLE('double')"
                raise AttributeError(msg)
            buf = bgl.Buffer(type, dim)
            glGet(template, buf)
        else:
            buf = bgl.Buffer(type, dim, template)

        if return_int:
            return buf[0]
        else:
            return buf


def glSwitch(attr, value):
    if value:
        bgl.glEnable(attr)
    else:
        bgl.glDisable(attr)


class GLSettings:
    def __init__(self, context, view_matrix=None, perspective_matrix=None):
        rv3d = context.region_data
        if view_matrix is None:
            if rv3d:
                view_matrix = rv3d.view_matrix
            else:
                view_matrix = Matrix.Identity(4)
        if perspective_matrix is None:
            if rv3d:
                perspective_matrix = rv3d.perspective_matrix
            else:
                perspective_matrix = Matrix.Identity(4)
        window_matrix = perspective_matrix * view_matrix.inverted()

        # type: <mathutils.Matrix>
        self.view_matrix = view_matrix
        self.window_matrix = window_matrix
        self.perspective_matrix = perspective_matrix

        # type: <bgl.Buffer>
        self.modelview_matrix = Buffer(
            'double', (4, 4), bgl.GL_MODELVIEW_MATRIX)
        self.projection_matrix = Buffer(
            'double', (4, 4), bgl.GL_PROJECTION_MATRIX)

        self._modelview_stack = []
        self._projection_stack = []
        self._modelview_bak_2d = None
        self._projection_bak_2d = None
        self._modelview_bak_3d = None
        self._projection_bak_3d = None

        region = context.region
        self.region_size = region.width, region.height

        # staticmethod
        self.Buffer = Buffer
        self.glSwitch = glSwitch

    # @staticmethod
    # def Buffer(type, dimensions=0, template=None):
    #     return Buffer(type, dimensions, template)

    # @staticmethod
    # def glSwitch(attr, value):
    #     glSwitch(attr, value)

    @staticmethod
    def mul_4x4_matrixd(m1, m2):
        """double型で大きさが16のBuffer同士の積"""
        matrix_mode = Buffer('int', 0, bgl.GL_MATRIX_MODE)
        bgl.glMatrixMode(bgl.GL_MODELVIEW)  # GL_MAX_MODELVIEW_STACK_DEPTH: 32
        bgl.glPushMatrix()
        bgl.glLoadMatrixd(m1)
        bgl.glMultMatrixd(m2)
        mat = Buffer('double', (4, 4), bgl.GL_MODELVIEW_MATRIX)
        bgl.glPopMatrix()
        bgl.glMatrixMode(matrix_mode)
        return mat

    @classmethod
    def get_matrix(cls, matrix_type, buffer=False):
        """GL_MODELVIEW_MATRIX, GL_PROJECTION_MATRIX を元にしたMatrixを返す。
        self.modelview_matrix等のインスタンス属性は使用しない。
        Spaceのコールバック関数の中でこのメソッドを呼んだ場合、
        PRE_VIEW / POST_VIEW と POST_PIXEL で違いがあるので十分注意すること。
        :param buffer: TrueだとBufferオブジェクトを返す。
        :rtype: Matrix | Buffer
        """
        if isinstance(matrix_type, int):
            if matrix_type == bgl.GL_MODELVIEW_MATRIX:
                matrix_type = 'modelview'
            elif matrix_type == bgl.GL_PROJECTION_MATRIX:
                matrix_type = 'projection'
            else:
                return None
        elif isinstance(matrix_type, str):
            matrix_type = matrix_type.lower()
        else:
            return None

        modelview = Buffer('double', (4, 4), bgl.GL_MODELVIEW_MATRIX)
        vmat = Matrix(modelview).transposed()
        if matrix_type.startswith(('model', 'view')):
            if buffer:
                return modelview
            else:
                return vmat
        else:
            projection = Buffer('double', (4, 4), bgl.GL_PROJECTION_MATRIX)
            wmat = Matrix(projection).transposed()
            if matrix_type.startswith(('proj', 'win')):
                if buffer:
                    return projection
                else:
                    return wmat
            elif matrix_type.startswith('pers'):
                if buffer:
                    return cls.mul_4x4_matrixd(projection, modelview)
                else:
                    return wmat * vmat

    @staticmethod
    def font_size(id=0, size=11, dpi=None):
        if dpi is None:
            dpi = bpy.context.user_preferences.system.dpi
        blf.size(id, size, dpi)

    def _load_matrix(self, modelview=None, projection=None):
        matrix_mode = Buffer('int', 0, bgl.GL_MATRIX_MODE)
        if modelview:
            bgl.glMatrixMode(bgl.GL_MODELVIEW)
            bgl.glLoadIdentity()  # glLoadMatrix()にも必須
            if isinstance(modelview, bgl.Buffer):
                bgl.glLoadMatrixd(modelview)
        if projection:
            bgl.glMatrixMode(bgl.GL_PROJECTION)
            bgl.glLoadIdentity()  # glLoadMatrix()にも必須
            if isinstance(projection, bgl.Buffer):
                bgl.glLoadMatrixd(projection)
        bgl.glMatrixMode(matrix_mode)

    def push(self, mask=bgl.GL_ALL_ATTRIB_BITS):
        """glPushAttrib()で状態変数を保存しておく。
        glPushMatrix(), glPopMatrix() は GL_MAX_MODELVIEW_STACK_DEPTH が 32
        なのに対し、GL_MAX_PROJECTION_STACK_DEPTH が 4 しか無い為、使用しない。
        """
        bgl.glPushAttrib(mask)
        self._modelview_stack.append(
            Buffer('double', (4, 4), bgl.GL_MODELVIEW_MATRIX))
        self._projection_stack.append(
            Buffer('double', (4, 4), bgl.GL_PROJECTION_MATRIX))

    def pop(self):
        """push()時の状態に戻す。"""
        self._load_matrix(self._modelview_stack.pop(),
                          self._projection_stack.pop())
        bgl.glPopAttrib()

    def prepare_3d(self):
        """POST_PIXELのcallbackでworld座標系を用いて描画する場合に使用する。"""
        self._modelview_bak_3d = Buffer('double', (4, 4),
                                        bgl.GL_MODELVIEW_MATRIX)
        self._projection_bak_3d = Buffer('double', (4, 4),
                                         bgl.GL_PROJECTION_MATRIX)
        view_mat = Buffer('double', (4, 4), self.view_matrix.transposed())
        win_mat = Buffer('double', (4, 4), self.window_matrix.transposed())
        self._load_matrix(view_mat, win_mat)

    def restore_3d(self):
        """prepare_3d()での変更を戻す"""
        self._load_matrix(self._modelview_bak_3d, self._projection_bak_3d)

    def prepare_2d(self):
        """PRE_VIEW,POST_VIEWのcallbackでscreen座標系を用いて描画する場合に
        使用する。
        参照: ED_region_do_draw() -> ED_region_pixelspace() ->
        wmOrtho2_region_pixelspace()

        """
        self._modelview_bak_2d = Buffer('double', (4, 4),
                                        bgl.GL_MODELVIEW_MATRIX)
        self._projection_bak_2d = Buffer('double', (4, 4),
                                         bgl.GL_PROJECTION_MATRIX)
        matrix_mode = Buffer('int', 0, bgl.GL_MATRIX_MODE)

        bgl.glMatrixMode(bgl.GL_PROJECTION)
        bgl.glLoadIdentity()  # 必須
        w, h = self.region_size
        # wmOrtho2_region_pixelspace(), wmOrtho2() 参照
        ofs = -0.01
        bgl.glOrtho(ofs, w + ofs, ofs, h + ofs, -100, 100)
        # bgl.glTranslated(GLA_PIXEL_OFS, GLA_PIXEL_OFS, 0.0)

        bgl.glMatrixMode(bgl.GL_MODELVIEW)
        bgl.glLoadIdentity()

        bgl.glMatrixMode(matrix_mode)

    def restore_2d(self):
        """prepare_2d()での変更を戻す"""
        self._load_matrix(self._modelview_bak_2d, self._projection_bak_2d)


def draw_circle(x, y, radius, subdivide, poly=False):
    r = 0.0
    dr = math.pi * 2 / subdivide
    if poly:
        subdivide += 1
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        bgl.glVertex2f(x, y)
    else:
        bgl.glBegin(bgl.GL_LINE_LOOP)
    for i in range(subdivide):
        bgl.glVertex2f(x + radius * math.cos(r), y + radius * math.sin(r))
        r += dr
    bgl.glEnd()


def draw_box(xmin, ymin, w, h, angle=0.0, poly=False, colors=None):
    """左下から反時計回りに描画。
    :param angle: 0.0以外なら(xmin, ymin)を中心に回転する
    :param colors: 各頂点に色を指定する[[R,G,B], ...] or [[R,G,B,A], ...]
    """
    coords = ((xmin, ymin),
              (xmin + w, ymin),
              (xmin + w, ymin + h),
              (xmin, ymin + h))
    if angle != 0.0:
        m = Matrix.Rotation(angle, 2)
        v = Vector(coords[0])
        coords = [m * (Vector(co) - v) + v for co in coords]

    bgl.glBegin(bgl.GL_QUADS if poly else bgl.GL_LINE_LOOP)
    if colors:
        glColor = bgl.glColor3f if len(colors[0]) == 3 else bgl.glColor4f
        for co, col in zip(coords, colors):
            glColor(*col)
            bgl.glVertex2f(*co)
    else:
        for co in coords:
            bgl.glVertex2f(*co)
    bgl.glEnd()


def draw_triangle(v1, v2, v3, poly=False):
    if len(v1) == 3:
        func = bgl.glVertex3f
    else:
        func = bgl.glVertex2f
    if poly:
        bgl.glBegin(bgl.GL_TRIANGLES)
    else:
        bgl.glBegin(bgl.GL_LINE_LOOP)
    func(*v1)
    func(*v2)
    func(*v3)
    bgl.glEnd()


def blf_draw(fontid, txt):
    blend = Buffer('bool', 0, bgl.GL_BLEND)
    tex2d = Buffer('bool', 0, bgl.GL_TEXTURE_2D)
    blf.draw(fontid, txt)
    glSwitch(bgl.GL_BLEND, blend)
    glSwitch(bgl.GL_TEXTURE_2D, tex2d)
