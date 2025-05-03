def is_audio_file(file_path):  
    """  
    检查文件是否为支持的音频格式  
    """  
    audio_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.m4a']  
    return any(file_path.lower().endswith(ext) for ext in audio_extensions)  
