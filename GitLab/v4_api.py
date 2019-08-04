import aiohttp


class Gitlab(object):
    def __init__(self, server: str, token: str):
        self.server = server if server.startswith(("http://", "https://")) else "https://" + server
        self.headers = {"Private-Token": token}
        self.project = ProjectManager(self)


class BaseManager(object):
    def __init__(self, gitlab: Gitlab):
        self.gitlab = gitlab
        self.headers = gitlab.headers
        self.server = gitlab.server
        self.session = aiohttp.ClientSession

    async def get(self, resource_id: int):
        _path = "{}/{}".format(self.path, resource_id)
        url = "{}/{}/{}".format(self.server, self.path, resource_id)
        print(url)
        async with self.session() as session:
            async with session.get(url, headers=self.headers) as resp:
                # print("status is ", resp.status)
                try:
                    body = await resp.json()
                except Exception as e:
                    print(e)
                    exit(2)
                if resp.status == 200:
                    # 返回的JSON数据，还要将Project对象给予相关属性以及Pipeline对象
                    obj = type(self.resource, (BaseManager, ), body)
                    attr = "pipelines"
                    attr_obj = type(attr, (BaseManager, ), {"resource": attr})(self.gitlab)
                    # attr_obj.path = "{}/{}".format(_path, attr)
                    attr_obj.path = "{}/{}".format(_path, attr)
                    # print(attr_obj.headers)
                    setattr(obj, attr, attr_obj)
                    return obj
                return {}

    async def all(self):
        pass

    async def search(self):
        pass


class ProjectManager(BaseManager):
    resource = "project"
    path = "/api/v4/projects"
    attrs = (
        "pipelines",
    )


async def main():
    import os
    gitlab = Gitlab(os.getenv("GIT_SERVER"), os.getenv("GIT_TOKEN"))
    project= await gitlab.project.get(37)
    pipeline = await project.pipelines.get(resource_id=250)
    print(dir(pipeline))


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())