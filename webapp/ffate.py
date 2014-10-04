import web

urls = (
    '/', 'index',
    '/cases', 'cases',
    '/search', 'search',
    '/add','add'
)

db = web.database(dbn='postgres', db='webpy', user='webpy', pw='')

render = web.template.render('/var/www/templates')

web.template.Template.globals.update(dict(
  render = render
))


class index:
    def GET(self):
        jenkins_url = web.ctx.homedomain + ":8080/"
        return render.tabbed("Forensicator FATE", jenkins_url)

class cases:
    def GET(self):
        return render.cases()

class add:
    def POST(self):
        i = web.input()
        n = db.insert('cases', casename=i.casename,memory_image=i.memory_image,disk_image=i.disk_image,disk_name=i.disk_name,timezone=i.timezone,volatility_profile=i.volatility_profile,notes=i.notes,case_keywords=i.case_keywords)
        raise web.seeother('/')

class search:
    def POST(self):
        i = web.input()
        print i
        return render.listing(db.select('cases',what='*',order='id',limit=10000))
    def GET(self):
        jenkins_url = web.ctx.homedomain + ":8080/"
        jenkins_job_url = jenkins_url + "job/findWindowsEvidence/buildWithParameters"
        return render.listing(db.select('cases',what='*',order='id',limit=10000), jenkins_job_url)


if __name__ == "__main__":
    app.run()


app = web.application(urls, globals())
application = app.wsgifunc()

