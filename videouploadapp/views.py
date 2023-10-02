import os
import tempfile
import moviepy.editor as mp
import speech_recognition as sr
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer

@api_view(['POST'])
def upload_video(request):
    if request.method == 'POST':
        video_data = request.FILES.get('video')
        if video_data:
            try:
                # Save video file to the FileField
                video_instance = Video(video_file=video_data)
                video_instance.save()

                # Perform automatic transcription
                video_file_path = video_instance.video_file.path
                video_clip = mp.VideoFileClip(video_file_path)
                audio_clip = video_clip.audio
                audio_clip.write_audiofile(video_file_path.replace('.mp4', '.wav'))

                recognizer = sr.Recognizer()
                with sr.AudioFile(video_file_path.replace('.mp4', '.wav')) as source:
                    audio_data = recognizer.record(source)
                    transcript = recognizer.recognize_google(audio_data)

                video_instance.transcript = transcript
                video_instance.save()

                serializer = VideoSerializer(video_instance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'No video data provided.'}, status=status.HTTP_400_BAD_REQUEST)
