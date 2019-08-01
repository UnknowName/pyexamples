import aiohttp


class BaseManagerNew(object):
    """
    相办法将相关资源的方法复用起来，不用每个资源对象都需要定义一系统方法
    """
    def __init__(self, gitlab: object, **kwarg):
        self.gitlab = gitlab
        self.kwarg = kwarg

    async def all(self):
        _name = self.kwarg.get("name")
        _path = "/api/v4/{}".format(_name)
        return await self.gitlab.get_all(_name, _path)

    async def get(self, kw: int):
        _path = "/api/v4/{}/{}".format(self.name, kw)

    async def delete(self):
        pass

    async def search(self):
        pass

    async def create(self):
        pass


class PipelineManagerNew(object):
    name = "pipelines"

    def __init__(self, gitlab: object, project: object):
        self.project = project
        self.gitlab = gitlab

    async def all(self):
        _path = "/api/v4/projects/{}/pipelines".format(self.project.id)
        return await self.gitlab.get_all(self.name, _path)

    async def delete(self, pipeline_id: int) -> bool:
        _path = "/api/v4/projects/{}/pipelines/{}".format(self.project.id, pipeline_id)
        status = await self.gitlab.delete(_path)
        if status == 204:
            return True
        else:
            return False


class ProjectManagerNew(object):
    name = "projects"

    def __init__(self, gitlab: object):
        self.gitlab = gitlab

    async def _add_attr(self, obj: object):
        pass

    async def all(self):
        _path = "/api/v4/projects"
        resps = await self.gitlab.get_all(self.name, _path)
        # 增加pipeline对象属性，这里后续也想办法优化
        [setattr(obj, "pipeline", PipelineManagerNew(self.gitlab, obj)) for obj in resps]
        return resps

    async def search(self, name: str):
        resps = await self.gitlab.search(self.name, name)
        # 增加pipeline对象属性，这里后续也想办法优化
        [setattr(obj, "pipeline", PipelineManagerNew(self.gitlab, obj)) for obj in resps]
        return resps


class GitlabAPI(object):
    session = aiohttp.ClientSession

    def __init__(self, server: str, token: str, token_type: str):
        self.server = server
        self._type = token_type
        if token_type == "private":
            self.headers = {"Private-Token": token}
        elif token_type == "oauth":
            self.headers = {"Oauth-Token": token}
        else:
            raise Exception("Token type not supported")
        self.project = ProjectManagerNew(self)

    async def delete(self, path: str):
        _url = "{}{}".format(self.server, path)
        async with self.session() as session:
            async with session.delete(_url, headers=self.headers) as resp:
                return resp.status

    async def _fetch(self, path: str) -> (aiohttp.ClientResponse.headers, aiohttp.ClientResponse.json):
        _url = "{}{}".format(self.server, path)
        async with self.session() as session:
            async with session.get(_url, headers=self.headers) as resp:
                return resp.headers, await resp.json()

    async def get_all(self, resource: str, path: str) -> list:
        # 类属性，用以确定资源类型构造URL请求
        totals = list()
        _headers, _resps = await self._fetch(path)
        if not isinstance(_resps, list):
            return []
        next_page = _headers.get("X-Next-Page")
        for _project in _resps:
            # 通过Type实例化对象，并赋于相关属性
            obj = type(resource.capitalize(), (), _project)
            totals.append(obj)
        # 默认只返回20条数据，检查是否还有内容
        while next_page:
            _next_path = "{}?page={}".format(path, next_page)
            _headers, _resps = await self._fetch(_next_path)
            for _obj in _resps:
                obj = type(resource.capitalize(), (), _obj)
                totals.append(obj)
            next_page = _headers.get("X-Next-Page")
        return totals

    async def search(self, resource: str, name: str) -> list:
        _path = "/api/v4/search?scope={}&search={}".format(resource, name)
        return await self.get_all(resource, _path)


async def main():
    import os
    g = GitlabAPI(os.getenv("GIT_SERVER"), os.getenv("GIT_TOKEN"), "private")
    # Get all projects in gitlab
    """
    all_projects = await g.project.all()
    print(len(all_projects))
    for project in all_projects:
        # print(hasattr(project, "pipeline"))
        pipelines = await project.pipeline.all()
        if not pipelines:
            continue
        else:
            print(pipelines)
    """
    # Get one project
    # project = await g.project.get(project_id=37)
    # Search one project
    projects = await g.project.search("daohao")
    for project in projects:
        if project.name == "daohao":
            # print(hasattr(project, "pipeline"))
            pipelines = await project.pipeline.all()
            if not pipelines:
                print("The project has no pipeline yet")
                exit(0)
            await project.pipeline.delete(pipelines[-1].id)

        else:
            print("Not Fond!")


if __name__ == '__main__':
    import asyncio
    import time
    start = time.time()
    asyncio.run(main())
    print(time.time() - start)
