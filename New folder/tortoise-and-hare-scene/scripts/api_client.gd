extends Node
var api_url := "http://127.0.0.1:8000/next"

func get_next_scene(current_scene: String, user_choice: String) -> Dictionary:
	var body = {"current_scene": current_scene, "user_choice": user_choice}
	var http := HTTPRequest.new()
	add_child(http)
	var error = http.request(api_url, [], HTTPClient.METHOD_POST, JSON.stringify(body))
	if error != OK:
		push_error("API request failed: %s" % error)
	await http.request_completed
	if http.get_response_code() == 200:
		var response = JSON.parse_string(http.get_body_as_string())
		return response
	else:
		push_warning("API error: %s" % http.get_response_code())
		return {}