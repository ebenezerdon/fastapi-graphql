from graphene import String, List, ObjectType

class CourseType(ObjectType):
  id = String(required=True)
  title = String(required=True)
  instructor = String(required=True)
  publish_date = String()

class InstructorType(ObjectType):
  id = String(required=True)
  name = String(required=True)
  gender = String()
  country = String()
