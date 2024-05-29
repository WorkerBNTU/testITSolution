from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Video
from .utils import create_video
import os
from django.conf import settings


def index(request):
    video_list = Video.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(video_list, 10)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'video/main.html', {'videos': videos})


def run_text(request):
    if request.method == 'GET':
        text = request.GET.get('text', '')
        if text:
            video_data = create_video(text, settings.MEDIA_ROOT)
            video = Video(title=video_data['title'], video_file=video_data['path'])
            video.save()

        return redirect('index')


def download_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    file_path = os.path.realpath(video.video_file.path)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response


def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.video_file.delete()
    video.delete()
    return redirect('index')
