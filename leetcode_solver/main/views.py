import imp
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render
from main.models import Queries
from django.template.response import TemplateResponse
from django.shortcuts import redirect
import requests
import json
import googleapiclient.discovery
from django.conf import settings
from django.shortcuts import redirect


# YouTube API key
DEVELOPER_KEY = settings.GOOGLE_API_KEY


def index(request):
    # User requests the home page
    if request.method == 'GET':
        return TemplateResponse(request, 'main/index.html', context={"example": "-- some data --", "example2": "-- some other data --"})

    elif request.method == 'POST':
        input_data = request.POST.get('search', False)
        if not input_data:
            return TemplateResponse(request, 'main/index.html', context={"example": "Error!"})

        return redirect(f'/problem/{input_data}')


def problem(request, id):

    # Queries.objects.all().delete()
    failed = False
    
    # Check if we already have this question's data
    try:
        result = Queries.objects.get(question_id=int(id))
        context={"id": result.question_id,
                "title": result.title,
                "url": result.question_url_slug,
                "categories": json.loads(result.topics),
                "difficulty": int(result.difficulty),
                "content": result.content,
                "videos": json.loads(result.videos),
                "relatedQuestions": json.loads(result.similar_questions)[:4]}

        return TemplateResponse(request, 'main/problem.html', context)

    except ValueError:
        try:
            result = Queries.objects.get(question_url_slug=id)
            context={"id": result.question_id,
                    "url": result.question_url_slug,
                    "title": result.title,
                    "categories": json.loads(result.topics),
                    "difficulty": int(result.difficulty),
                    "content": result.content,
                    "videos": json.loads(result.videos),
                    "relatedQuestions": json.loads(result.similar_questions)[:4]}

            return TemplateResponse(request, 'main/problem.html', context)
        except Queries.DoesNotExist:
            failed = True
    except Queries.DoesNotExist:
        failed = True
    
    if failed:
        # If we don't have this question's data

        resp = requests.get('https://leetcode.com/api/problems/all/')
        questions = json.loads(resp.content)

        for question in questions['stat_status_pairs']:

            if id == question['stat']['question_id'] or id == question['stat']['question__article__slug']:

                paid_only = question['paid_only']

                if not paid_only:
                    
                    print("--- Getting API Data ---")

                    # Get basic question data
                    question_url_slug = question['stat']['question__article__slug']
                    difficulty = question['difficulty']['level']
                    question_title = question['stat']['question__title']

                    # Get specific question data
                    data = {"operationName": "questionData", "variables": {"titleSlug": question_url_slug}, "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}
                    resp = requests.post(
                        'https://leetcode.com/graphql', json=data).json()

                    try:
                        content = resp['data']['question']['content']
                        similar_questions = resp['data']['question']['similarQuestions']
                        topics = resp['data']['question']['topicTags']
                    except:
                        return TemplateResponse(request, 'main/error.html')

                    # Get YouTube API Data
                    SEARCH_QUERY = question_title + \
                        ' Leetcode ' + str(id) + ' Solution'

                    api_service_name, api_version = "youtube", "v3"

                    youtube = googleapiclient.discovery.build(
                        api_service_name, api_version, developerKey=DEVELOPER_KEY)

                    api_request = youtube.search().list(
                        part="id,snippet",
                        type='video',
                        q=SEARCH_QUERY,
                        videoDuration='short',
                        videoDefinition='high',
                        maxResults=4
                    )

                    response = api_request.execute()

                    videos = []
                    for item in response['items']:
                        video_title = item['snippet']['title']
                        video_description = item['snippet']['description']
                        channel_title = item['snippet']['channelTitle']
                        channel_url = 'https://www.youtube.com/channel/' + \
                            item['snippet']['channelId']
                        video_url = 'https://www.youtube.com/embed/' + \
                            item['id']['videoId']
                        thumbnail = item['snippet']['thumbnails']['high']['url']
                        videos.append({"video_title": video_title, 'video_desc': video_description,
                                    "channel_title": channel_title, "channel_url": channel_url, 'video_url': video_url, 'thumbnail': thumbnail})


                    q = Queries(question_id=question['stat']['question_id'], question_url_slug=question_url_slug, difficulty=difficulty, content=content, similar_questions = similar_questions, topics = json.dumps(topics), videos = json.dumps(videos), title = question_title)
                    q.save()

                    return TemplateResponse(request, 'main/problem.html',
                                            context={"id": question['stat']['question_id'],
                                                    "url": question_url_slug,
                                                    "title": question_title,
                                                    "categories": topics,
                                                    "difficulty": difficulty,
                                                    "content": content,
                                                    "videos": videos,
                                                    "relatedQuestions": json.loads(similar_questions)[:4]})
                else:
                    # Handle Premium Question
                    return TemplateResponse(request, 'main/error.html')

        return TemplateResponse(request, 'main/error.html')
