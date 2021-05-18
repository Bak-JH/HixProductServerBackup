from locust import HttpUser, TaskSet, task
import urllib3

urllib3.disable_warnings()

class UserBehavior(TaskSet):
    csrf_token = ''

    @task(1)
    def dashboard(self):
        r = self.client.get('https://services.hix.co.kr/product/login/', verify=False)
        self.csrf_token = r.cookies['csrftoken']
        self.client.headers['Referer'] = self.client.base_url
        r = self.client.post("https://services.hix.co.kr/order/?product=dentslicer", data={'billing_id' : '60176037238684001f8fb2f2', 'csrfmiddlewaretoken': self.csrf_token}, verify=False, auth=('admin', 'admin'))

        print(r)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 5
    max_wait = 1000