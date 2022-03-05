import imp
from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
import requests
import json
import googleapiclient.discovery
from django.conf import settings

# YouTube API key
DEVELOPER_KEY = settings.GOOGLE_API_KEY

def index(request):
    # User requests the home page
    if request.method == 'GET':
        return TemplateResponse(request, 'main/index.html', context={"example": "-- some data --", "example2": "-- some other data --"})

    elif request.method == 'POST':

        pass


def problem(request, id):
    # Get Leetcode API Data
    resp = requests.get('https://leetcode.com/api/problems/all/')
    questions = json.loads(resp.content)

    for question in questions['stat_status_pairs']:

        if id == question['stat']['question_id']:
            paid_only = question['paid_only']

            if not paid_only:

                # Get basic question data
                question_url_slug = question['stat']['question__article__slug']
                difficulty = question['difficulty']['level']
                question_title = question['stat']['question__title']

                # Get specific question data
                data = {"operationName": "questionData", "variables": {"titleSlug": question_url_slug}, "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}
                resp = requests.post(
                    'https://leetcode.com/graphql', json=data).json()

                content = resp['data']['question']['content']
                similar_questions = resp['data']['question']['similarQuestions']
                topics = resp['data']['question']['topicTags']
                stats = resp['data']['question']['stats']

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
                    video_url = 'https://www.youtube.com/watch?v=' + \
                        item['id']['videoId']
                    videos.append({"video_title": video_title, 'video_desc': video_description,
                                  "channel_title": channel_title, "channel_url": channel_url, 'video_url': video_url})

                output = {"question_url_slug": question_url_slug, "difficulty": difficulty, "question_title": question_title,
                          "content": content, "similar_questions": similar_questions, "topics": topics, "stats": stats, 'videos': videos}

                # TODO: Return the successfull template response
                return TemplateResponse(request, 'main/index.html', context={"youtube_link": id, "id": id})

            else:
                # Handle Premium Question
                # TODO: Offer another question up instead.
                return HttpResponse('<h1>Premium Only!</h1>')

    # TODO: Handle when the user puts in bad data as the id, or id is not a leetcode question
    return TemplateResponse(request, 'main/index.html', context={"youtube_link": id, "id": id})

