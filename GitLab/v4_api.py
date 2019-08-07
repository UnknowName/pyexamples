import aiohttp


class Gitlab(object):
    def __init__(self, server: str, token: str):
        self.server = server.rstrip("/") if server.startswith(("http://", "https://")) else "https://" + server
        self.headers = {"Private-Token": token}
        self.project = ProjectManager(self)


class BaseManager(object):
    def __init__(self, gitlab: Gitlab):
        self.gitlab = gitlab
        self.headers = gitlab.headers
        self.server = gitlab.server
        self.session = aiohttp.ClientSession

    def _add_attr(self, base_url: str, resource_name: str, dict_resp: dict):
        obj = type(resource_name, (BaseManager,), dict_resp)
        if hasattr(self, "attrs"):
            for attr in self.attrs:
                attr_obj = type(attr, (BaseManager,), {"resource": attr})(self.gitlab)
                if str(obj.id) in base_url:
                    attr_obj.path = "{}/{}".format(base_url, attr)
                else:
                    attr_obj.path = "{}/{}/{}".format(base_url, obj.id, attr)
                setattr(obj, attr, attr_obj)
        return obj

    async def _fetch(self, url: str):
        async with self.session() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.headers.get("Content-Type", "") == "application/json" and resp.status == 200:
                    response = await resp.json()
                    next_page = resp.headers.get("X-Next-Page")
                    # 如果是List，说明返回的有许多，用于all/search复用
                    if isinstance(response, list):
                        # search方法也会用到该方法，但search方法的URL并不能直接追加。这里进行判断，并修改为资源的根目录
                        if "/api/v4/search" in url:
                            url = "/api/v4/{}".format(self.resource)
                        return next_page, [
                            self._add_attr(base_url=url, resource_name=self.resource, dict_resp=_resp)
                            for _resp in response
                        ]
                    else:
                        obj = self._add_attr(base_url=url, resource_name=self.resource, dict_resp=response)
                        return next_page, obj
            return None, None

    async def get(self, resource_id: int):
        if self.server in self.path:
            url = "{}/{}".format(self.path, resource_id)
        else:
            url = "{}{}/{}".format(self.server, self.path, resource_id)
        # print("Get URL is ", url)
        _, obj = await self._fetch(url)
        return obj

    async def delete(self, resource_id: int):
        if self.server in self.path:
            url = "{}/{}".format(self.path, resource_id)
        else:
            url = "{}{}/{}".format(self.server, self.path, resource_id)
        # print("Delete URL is ", url)
        async with self.session() as sessoin:
            async with sessoin.delete(url, headers=self.headers) as resp:
                if resp.status == 204 and (await resp.text() == 1):
                    return True
                import sys
                sys.stdout.write("\033[93mWarning: Delete Failed, Reason: {}\033[0m\n".format(await resp.text()))
                return None

    async def all(self):
        if self.server in self.path:
            url = self.path
        else:
            url = "{}{}".format(self.server, self.path)
        next_page,  resp = await self._fetch(url)
        # print("All URL is ", url)
        totals = resp
        while next_page:
            next_page, objects = await self._fetch("{}?page={}".format(url, next_page))
            totals += objects
        return totals

    async def search(self, name: str):
        _url = "{}/api/v4/search?scope={}&search={}".format(self.server, self.resource, name)
        next_page, resp = await self._fetch(_url)
        # print("Search URL is ", _url)
        totals = resp
        while next_page:
            next_page, objects = await self._fetch("{}?page={}".format(url, next_page))
            totals += objects
        return totals


class ProjectManager(BaseManager):
    resource = "projects"
    path = "/api/v4/projects"
    attrs = (
        "pipelines",
    )


async def main():
    import os
    gitlab = Gitlab(os.getenv("GIT_SERVER"), os.getenv("GIT_TOKEN"))
    """"
    # Get single project and the project's pipelines
    project = await gitlab.project.get(37)
    pipeline = await project.pipelines.get(resource_id=259)
    if pipeline:
        print("Pipeline duration is ", pipeline.duration)
    # Get all projects
    projects = await gitlab.project.all()
    print("Total projects is ", len(projects))
    # Get all project's pipelines
    pipelines = await projects[0].pipelines.all()
    print("Project pipeline is ", pipelines)
    project = await gitlab.project.get(37)
    pipelines = await project.pipelines.all()
    if pipelines:
        await project.pipelines.delete(pipelines[-1].id)
        print("Delete Pipeline success")
    else:
        print("The project seems no pipeline yet")
    """
    # Search project by keyword daohao
    projects = await gitlab.project.search("daohao")
    project = projects[0]
    pipelines = await project.pipelines.all()
    await project.pipelines.delete(pipelines[-1])


if __name__ == '__main__':
    import time
    import asyncio
    start = time.time()
    asyncio.run(main())
    print(time.time() - start)
