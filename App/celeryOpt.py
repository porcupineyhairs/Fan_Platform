# encoding: utf-8
"""
@auth: cyq
@name: tasks
@desc: tasks
"""

from App import create_app
from App.celery import create_celery_app
from Model.Models import UICase

celery = create_celery_app(create_app())


#celery -A App.celeryOpt:celery  worker -E  -l info


@celery.task
def testCelery(x, y):
    print(x + y)


@celery.task
def runCase(caseId):
    case = UICase.get(caseId)
    info = case.caseInfo
    from comments.driverOpt import DriverOpt

    driver = DriverOpt(headless=info['headless'])
    driver.run(caseId, info['steps'])
