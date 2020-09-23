from graphene import ObjectType, List, String, Field, Schema, Mutation
from graphql.execution.executors.asyncio import AsyncioExecutor
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from schemas import CourseType, InstructorType
import json

app = FastAPI()
app.add_route("/", GraphQLApp(
  schema=Schema(),
  executor_class=AsyncioExecutor)
)
