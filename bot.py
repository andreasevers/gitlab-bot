from gidgetlab.aiohttp import GitLabBot

bot = GitLabBot(os.environ["GL_ACCOUNT"])

########################################################################################################################

@bot.router.register("Issue Hook", action="open")
async def issue_opened_event(event, gl, *args, **kwargs):
    """Whenever an issue is opened, apply the right labels."""
    titles = evaluate_open_labels(event.data['labels'])
    print(f"Current milestone_id: {event.object_attributes['milestone_id']}")
    url = f"/projects/{event.project_id}/issues/{event.object_attributes['iid']}?labels={titles}&milestone_id=1185388"
    await gl.put(url)
    """Whenever an issue is opened, greet the author and say thanks."""
    url = f"/projects/{event.project_id}/issues/{event.object_attributes['iid']}/notes"
    message = f"Thanks for the report @{event.data['user']['username']}! I will look into it ASAP! (I'm a bot)."
    await gl.post(url, data={"body": message})

def evaluate_open_labels(labels):
    return ', '.join(add_open_label_titles(list(filter(filter_open_label_titles, map(extract_open_label_title, labels)))))

def extract_open_label_title(label):
    return label['title']

def filter_open_label_titles(title):
    titlesToBeRemoved = ['Doing', 'Test', 'Done']
    if title in titlesToBeRemoved:
        return False
    else:
        return True

def add_open_label_titles(titles):
    additions = ['To%20Do', 'Superduper']
    return titles + additions

########################################################################################################################

@bot.router.register("Issue Hook", action="close")
async def issue_closed_event(event, gl, *args, **kwargs):
    """Whenever an issue is closed, apply the right labels."""
    titles = evaluate_closed_labels(event.data['labels'])
    url = f"/projects/{event.project_id}/issues/{event.object_attributes['iid']}?labels={titles}&assignee_ids[]=684917"
    await gl.put(url)
    """Whenever an issue is closed, let the PM follow up."""
    url = f"/projects/{event.project_id}/issues/{event.object_attributes['iid']}/notes"
    message = f"Thanks for closing the report @{event.data['user']['username']}! I will validate it ASAP! (I'm a bot)."
    await gl.post(url, data={"body": message})

def evaluate_closed_labels(labels):
    return ', '.join(add_closed_label_titles(list(filter(filter_closed_label_titles, map(extract_closed_label_title, labels)))))

def extract_closed_label_title(label):
    return label['title']

def filter_closed_label_titles(title):
    titlesToBeRemoved = ['Doing', 'Superduper','To Do']
    if title in titlesToBeRemoved:
        return False
    else:
        return True

def add_closed_label_titles(titles):
    additions = ['Done']
    return titles + additions

########################################################################################################################

if __name__ == "__main__":
    bot.run()