from celery.task import task


@task
def board_iteration(iteration):
    print "this is task " + str(iteration)