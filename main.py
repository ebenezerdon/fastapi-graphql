from graphene import ObjectType, List, String, Field, Schema, Mutation
from graphql.execution.executors.asyncio import AsyncioExecutor
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from schemas import CourseType, InstructorType
import json

class Query(ObjectType):
  course_list = None
  get_course = Field(List(CourseType), id=String())

  async def resolve_get_course(self, info, id=None):
    with open("./courses.json") as courses:
      course_list = json.load(courses)
    if (id):
      for course in course_list:
        if course['id'] == id: return [course]
    return course_list

class CreateCourse(Mutation):
  course = Field(CourseType)

  class Arguments:
    id = String(required=True)
    title = String(required=True)
    instructor = String(required=True)
    publish_date = String()

  async def mutate(self, info, id, title, instructor):
    with open("./courses.json", "r+") as courses:
      course_list = json.load(courses)

      for course in course_list:
        if course['id'] == id:
          raise Exception('Course with provided id already exists!')

      course_list.append({"id": id, "title": title, "instructor": instructor})
      courses.seek(0)
      json.dump(course_list, courses, indent=2)
    return CreateCourse(course=course_list[-1])

class UpdateCourse(Mutation):
  course = Field(CourseType)

  class Arguments:
    id = String(required=True)
    title = String(required=True)
    instructor = String(required=True)
    publish_date = String()

  async def mutate(self, info, id, title, instructor):
    with open("./courses.json", "r+") as courses:
      course_list = json.load(courses)

      for course in course_list:
        if course['id'] == id:
          indexOfCourse = course_list.index(course)
          course_list[indexOfCourse] = {"id": id, "title": title, "instructor": instructor}
          courses.seek(0)
          courses.truncate()

          json.dump(course_list, courses, indent=2)
    return UpdateCourse(course=course_list[indexOfCourse])

class Mutation(ObjectType):
  create_course = CreateCourse.Field()
  Update_course = UpdateCourse.Field()

app = FastAPI()
app.add_route("/", GraphQLApp(
  schema=Schema(query=Query, mutation=Mutation),
  executor_class=AsyncioExecutor)
)
