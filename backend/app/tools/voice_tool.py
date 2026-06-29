class VoiceTool:
    """
    Mock voice processing tool. Transcribes audio input streams/files.
    """
    def transcribe_audio(self, audio_file_path: str) -> str:
        # In a real environment, we'd use Speech-to-Text or Gemini multimodal audio transcription.
        # Since this is a mock tool, we return a transcription corresponding to the test case or a generic warning.
        print(f"Transcribing audio file from: {audio_file_path}")
        return "I need to find a cheap diabetic clinic near me and my father keeps forgetting his daily Metformin dose."
