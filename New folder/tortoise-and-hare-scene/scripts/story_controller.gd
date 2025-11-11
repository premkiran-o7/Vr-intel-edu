extends Node

# --- Configurable Scene List ---
@export var scenes: Array[String] = [
	"res://scenes/peaceful_morning_scene.tscn",
	"res://scenes/pebble_path_scene.tscn",
	"res://scenes/shiny_stream_scene.tscn",
	"res://scenes/lesson_scene.tscn"
]

# --- Timing Controls ---
@export var fade_duration: float = 1.5
@export var scene_duration: float = 8.0

# --- Runtime Variables ---
var current_scene_index: int = 0
var current_scene_instance: Node3D = null
@onready var fade_rect: ColorRect = $FadeRect
@onready var scene_holder: Node = $SceneHolder


# --- Initialization ---
func _ready() -> void:
	print("\n🚀 Story Controller Initialized")
	print("🎞 Loaded Scene List:", scenes)

	if fade_rect == null:
		push_error("❌ FadeRect missing under StoryController!")
		return
	if scene_holder == null:
		push_error("❌ SceneHolder missing under StoryController!")
		return

	fade_rect.visible = true
	fade_rect.color = Color(0, 0, 0, 1)
	fade_rect.z_index = 9999  # ✅ Always render above 3D content

	await fade_in_from_black()
	await get_tree().create_timer(0.5).timeout
	await play_next_scene()

"""
var result = await api_client.get_next_scene(current_scene_name, player_choice)
if result.has("next_scene"):
    load_scene(result["next_scene"])
    update_narration(result["narration"])
"""

# --- Sequential Scene Playback ---
func play_next_scene() -> void:
	print("\n🎬 Loading next scene...")

	# Clean up old scene
	if current_scene_instance and is_instance_valid(current_scene_instance):
		print("🗑 Removing previous scene:", current_scene_instance.name)
		current_scene_instance.queue_free()
		await get_tree().process_frame  # allow cleanup

	# Check if all scenes done
	if current_scene_index >= scenes.size():
		print("✅ All scenes completed — fading to black.")
		await fade_out_to_black()
		return

	# Load next scene
	var scene_path: String = scenes[current_scene_index]
	print("🎥 Attempting to load:", scene_path)

	var packed_scene: PackedScene = load(scene_path)
	if packed_scene == null:
		push_warning("⚠️ Scene load failed: " + scene_path)
		current_scene_index += 1
		await play_next_scene()
		return

	# Instantiate and add scene
	current_scene_instance = packed_scene.instantiate()
	scene_holder.add_child(current_scene_instance)
	print("✅ Scene loaded successfully:", current_scene_instance.name)

	# Keep fade rect visually above all scenes
	fade_rect.z_index = 9999

	# Fade in scene
	await fade_in_from_black()
	print("🌄 Scene is now visible.")

	# Auto-play scene animation if found
	var anim_player: AnimationPlayer = current_scene_instance.get_node_or_null("AnimPlayer")
	if anim_player:
		await get_tree().process_frame  # ensure animation is ready

		var libraries: Array = anim_player.libraries.keys()
		if libraries.size() > 0:
			var lib_key = libraries[0]
			var animation_library: AnimationLibrary = anim_player.libraries[lib_key]
			var anim_names: Array = animation_library.get_animation_list()
			if anim_names.size() > 0:
				var anim_name: String = anim_names[0]
				anim_player.play(anim_name)
				print("🎞 Playing animation:", anim_name)

	# Fade in narration text
	var narration_label: Label3D = current_scene_instance.get_node_or_null("NarrationText")
	if narration_label:
		await fade_text_in(narration_label)

	# Wait for scene duration
	await get_tree().create_timer(scene_duration).timeout
	print("🕓 Scene duration complete — preparing transition.")

	# Fade out narration
	if narration_label:
		await fade_text_out(narration_label)

	# Fade out scene and load next
	await fade_out_to_black()
	current_scene_index += 1
	await play_next_scene()


# --- Fade Helpers ---
func fade_in_from_black() -> void:
	fade_rect.visible = true
	fade_rect.modulate.a = 1.0
	print("🔆 Fading in...")

	var tween: Tween = create_tween()
	tween.tween_property(fade_rect, "modulate:a", 0.0, fade_duration)
	await tween.finished

	fade_rect.visible = false
	print("✅ Fade-in complete.")


func fade_out_to_black() -> void:
	fade_rect.visible = true
	fade_rect.modulate.a = 0.0
	print("🌙 Fading out...")

	var tween: Tween = create_tween()
	tween.tween_property(fade_rect, "modulate:a", 1.0, fade_duration)
	await tween.finished

	print("✅ Fade-out complete.")


# --- Text Fade Helpers ---
func fade_text_in(label: Label3D) -> void:
	if not label:
		return
	label.modulate.a = 0.0
	label.visible = true
	print("📝 Fading text in:", label.text)

	var tween: Tween = create_tween()
	tween.tween_property(label, "modulate:a", 1.0, 1.5)
	await tween.finished


func fade_text_out(label: Label3D) -> void:
	if not label:
		return
	print("💨 Fading text out:", label.text)

	var tween: Tween = create_tween()
	tween.tween_property(label, "modulate:a", 0.0, 1.0)
	await tween.finished
	label.visible = false
