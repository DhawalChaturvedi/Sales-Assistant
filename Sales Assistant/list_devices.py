import sounddevice as sd

print("\n🎙️ Available Audio Devices:\n")
for i, device in enumerate(sd.query_devices()):
    print(f"[{i}] {device['name']} | Inputs: {device['max_input_channels']}, Outputs: {device['max_output_channels']}")
