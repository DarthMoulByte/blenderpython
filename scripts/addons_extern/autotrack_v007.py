bl_info = {
    "name": "Autotrack",
    "author": "Miika Puustinen, Matti Kaihola",
    "version": (0, 7),
    "blender": (2, 78, 0),
    "location": "Movie clip Editor > Tools Panel > Autotrack",
    "description": "Motion Tracking with automatic feature detection.",
    "warning": "",
    "wiki_url": "",
    "category": "Motion Tracking",
    }


import bpy
import math


class ModalTimerOperator(bpy.types.Operator):
    """Autotrack. Esc to cancel."""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    limits = bpy.props.IntProperty(default=0)
    _timer = None

    def active_clip(self):
        area = [i for i in bpy.context.screen.areas if i.type == 'CLIP_EDITOR'][0]
        clip = area.spaces.active.clip.name
        return clip

    # DETECT FEATURES
    def auto_features(self, delete_threshold, limits):
        tracks = []
        selected = []
        old = []
        to_delete = []

        bpy.ops.clip.select_all(action='DESELECT')

        # Detect Features
        bpy.ops.clip.detect_features(
            threshold=bpy.context.scene.df_threshold,
            min_distance=bpy.context.scene.df_distance,
            margin=bpy.context.scene.df_margin,
            placement=bpy.context.scene.placement_list
            )

        current_frame = bpy.context.scene.frame_current

        tracks = bpy.data.movieclips[self.active_clip()].tracking.tracks
        for track in tracks:
            if track.markers.find_frame(current_frame) is not None:
                if track.select is not True and track.hide is False and track.markers.find_frame(current_frame).mute is False:
                    old.append(track)
                if track.select is True:
                    selected.append(track)

        # Select overlapping new markers
        for i in selected:
            for j in old:
                i_marker = i.markers.find_frame(current_frame)
                j_marker = j.markers.find_frame(current_frame)
                distance = math.sqrt(((i_marker.co[0] - j_marker.co[0])**2) + ((i_marker.co[1] - j_marker.co[1])**2))
                # print(distance)
                if distance < delete_threshold:
                    to_delete.append(i)
                    break

        # delete short tracks
        for track in tracks:
            muted = []
            active = []
            # print(track)
            for marker in track.markers:
                if marker.mute is True:
                    muted.append(marker)
                else:
                    active.append(marker)
            if len(muted) > 3 and len(active) < 1:
                to_delete.append(track)

            if len(track.markers) > 1 and len(active) == 0:
                to_delete.append(track)

        # Delete Overlapping Markers
        bpy.ops.clip.select_all(action='DESELECT')
        for track in tracks:
            if track in to_delete:
                track.select = True

        bpy.ops.clip.delete_track()
        track_amount = len(bpy.data.movieclips[self.active_clip()].tracking.tracks)
        print(str(len(selected)) + "/" + str(len(tracks)) + " tracks tracking.")

    # AUTOTRACK FRAMES
    def track_frames_backward(self):
        bpy.ops.clip.track_markers(backwards=True, sequence=False)

    def track_frames_forward(self):
        bpy.ops.clip.track_markers(backwards=False, sequence=False)

    # REMOVE BAD MARKERS
    def remove_extra(self, angle_cut, jump_cut, track_backwards):
        trackers = []

        if track_backwards is True:
            one_frame = -1
            two_frames = -2
        else:
            one_frame = 1
            two_frames = 2

        if self.limits >= 3:
            trackers = bpy.data.movieclips[self.active_clip()].tracking.tracks

            for i in trackers:
                if len(i.markers) > 5:
                    current_frame = bpy.context.scene.frame_current

                    if (i.markers.find_frame(current_frame) is not None and
                       i.markers.find_frame(current_frame - one_frame) is not None and
                       i.markers.find_frame(current_frame - two_frames) is not None):

                        key_frame = i.markers.find_frame(current_frame).co.normalized()
                        prev_frame = i.markers.find_frame(current_frame - one_frame).co.normalized()
                        origo_frame = i.markers.find_frame(current_frame - two_frames).co.normalized()

                        a = (key_frame - origo_frame).normalized()
                        b = (prev_frame - origo_frame).normalized()
                        angle = abs(math.degrees(math.atan2(b[1], b[0]) - math.atan2(a[1], a[0])))
                        # print('angle is {}'.format(angle))

                        key_frame = i.markers.find_frame(current_frame).co
                        prev_frame = i.markers.find_frame(current_frame - one_frame).co

                        distance = math.sqrt(((key_frame[0] - prev_frame[0])**2) + ((key_frame[1] - prev_frame[1])**2))

                        if distance > jump_cut:
                            if (i.markers.find_frame(current_frame) is not None and
                               i.markers.find_frame(current_frame - one_frame) is not None):

                                # create new track to new pos
                                new_track = \
                                    bpy.data.movieclips[self.active_clip()].tracking.tracks.new(frame=current_frame)
                                new_track.markers[0].co = i.markers.find_frame(current_frame).co
                                i.markers.find_frame(current_frame).mute = True
                                i.markers.find_frame(current_frame - one_frame).mute = True
                        if angle_cut > 0 or angle_cut < 360:
                            if angle > angle_cut:
                                if (i.markers.find_frame(current_frame) is not None and
                                   i.markers.find_frame(current_frame - one_frame) is not None):

                                    i.markers.find_frame(current_frame).mute = True
                                    i.markers.find_frame(current_frame - one_frame).mute = True

    def modal(self, context, event):
        scene = bpy.context.scene
        if (event.type in {'ESC'} or scene.frame_current == scene.frame_end + 1 or
           scene.frame_current == scene.frame_start - 1):
            self.limits = 0
            self.cancel(context)
            return {'FINISHED'}

        if event.type == 'TIMER':

            # PROP VARIABLES
            delete_threshold = bpy.context.scene.delete_threshold
            endframe = bpy.context.scene.frame_end
            start_frame = bpy.context.scene.frame_start
            frame_separate = bpy.context.scene.frame_separation
            margin = bpy.context.scene.df_margin
            distance = bpy.context.scene.df_distance
            threshold = bpy.context.scene.df_threshold
            angle_cut = bpy.context.scene.angle_cut
            jump_cut = bpy.context.scene.jump_cut
            track_backwards = bpy.context.scene.track_backwards

            # Auto features every frame separate step
            if bpy.context.scene.frame_current % frame_separate == 0 or self.limits == 0:
                limits = self.limits
                self.auto_features(delete_threshold, limits)

            # Select all trackers for tracking
            select_all = bpy.ops.clip.select_all(action='SELECT')
            tracks = bpy.data.movieclips[self.active_clip()].tracking.tracks
            active_tracks = []
            for track in tracks:
                if track.lock is True:
                    track.select = False
                else:
                    active_tracks.append(track)

            # Forwards or backwards tracking
            if track_backwards is True:
                if len(active_tracks) == 0:
                    print("No new tracks created. Doing nothing.")
                    self.limits = 0
                    self.cancel(context)
                    return {'FINISHED'}
                else:
                    self.track_frames_backward()
            else:
                if len(active_tracks) == 0:
                    print("No new tracks created. Doing nothing.")
                    self.limits = 0
                    self.cancel(context)
                    return {'FINISHED'}
                else:
                    self.track_frames_forward()

            # Remove bad tracks
            self.remove_extra(angle_cut, jump_cut, track_backwards)

            self.limits += 1

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(time_step=0.5, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


# UI CREATION #

class tracking_autotracker(bpy.types.Panel):
    """Creates a Panel in the Render Layer properties window"""
    bl_label = "Autotrack"
    bl_idname = "autotrack"
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = "Track"

    # Draw UI
    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.scale_y = 1.5
        # props = row.operator("clip.track_markers", text="Backwards",icon='PLAY_REVERSE')

        props = row.operator("wm.modal_timer_operator", text="Autotrack!     ", icon='PLAY')

        row = layout.row(align=True)
        row.prop(context.scene, "track_backwards")

        row = layout.row(align=True)  # make next row
        row.prop(context.scene, "delete_threshold")

        row = layout.row(align=True)
        row.prop(context.scene, "frame_separation", text="Frame Separation")

        row = layout.row(align=True)
        row.prop(context.scene, "jump_cut", text="Jump Threshold")

        row = layout.row(align=True)
        row.prop(context.scene, "angle_cut", text="Angle Threshold")

        row = layout.row(align=True)
        row.label(text="Detect Features Settings:")

        row = layout.row(align=True)
        row.prop(context.scene, "df_margin", text="Margin:")

        row = layout.row(align=True)
        row.prop(context.scene, "df_threshold", text="Threshold:")

        row = layout.row(align=True)
        row.prop(context.scene, "df_distance", text="Distance:")

        row = layout.row(align=True)
        row.label(text="Detect Features Settings:")

        row = layout.row(align=True)  # make next row
        row.prop(context.scene, "placement_list")


# REGISTER BLOCK #
def register():
    bpy.utils.register_class(ModalTimerOperator)
    bpy.utils.register_class(tracking_autotracker)

    # Registering properties
    bpy.types.Scene.df_margin = bpy.props.IntProperty(
            name="Detect Features Margin",
            description="Only features further margin pixels from the image edges are concidered.",
            default=16,
            min=0,
            max=2000
            )
    bpy.types.Scene.df_threshold = bpy.props.FloatProperty(
            name="Detect Features Threshold",
            description="Threshold level to concider feature good enough for tracking.",
            default=0.01,
            min=0.0,
            max=1.0
            )

    bpy.types.Scene.df_distance = bpy.props.IntProperty(
            name="Detect Features Distance",
            description="Minimal distance accepted between two features.",
            default=64,
            min=1,
            max=300
            )

    bpy.types.Scene.delete_threshold = bpy.props.FloatProperty(
            name="New Marker Threshold",
            description="Threshold how near new features can appear during autotracking.",
            default=0.1,
            min=0.0,
            max=1.0
            )

    bpy.types.Scene.frame_separation = bpy.props.IntProperty(
            name="Frame Separation",
            description="How often new features are generated.",
            default=5,
            min=1,
            max=100
            )
            
    bpy.types.Scene.jump_cut = bpy.props.FloatProperty(
            name="Jump Cut",
            description="Distance how much a marker can travel before it is concidered "
                        "to be a bad track and cut. A new track is added.",
            default=0.1,
            min=0.0,
            max=1.0
    )

    bpy.types.Scene.angle_cut = bpy.props.IntProperty(
            name="Angle Cut",
            description="*EXPIRIMENTAL* Angle how much a tracker can turn before "
                        "it is concidered to be a bad track and being muted.",
            default=360,
            min=0,
            max=360
            )

    bpy.types.Scene.track_backwards = bpy.props.BoolProperty(
            name="AutoTrack Backwards",
            description="Autotrack backwards.",
            default=False
    )

    # Dropdown menu
    list_items = [
        ("FRAME", "Whole Frame", "", 1),
        ("INSIDE_GPENCIL", "Inside Grease Pencil", "", 2),
        ("OUTSIDE_GPENCIL", "Outside Grease Pencil", "", 3),
    ]

    bpy.types.Scene.placement_list = bpy.props.EnumProperty(
            name="",
            description="Feaure Placement",
            items=list_items
            )


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)
    bpy.utils.unregister_class(tracking_autotracker)
    del bpy.types.Scene.df_margin
    del bpy.types.Scene.df_threshold
    del bpy.types.Scene.df_distance
    del bpy.types.Scene.delete_threshold
    del bpy.types.Scene.frame_separation
    del bpy.types.Scene.jump_cut
    del bpy.types.Scene.angle_cut
    del bpy.types.Scene.track_backwards
    del bpy.types.Scene.placement_list


if __name__ == "__main__":
    register()
