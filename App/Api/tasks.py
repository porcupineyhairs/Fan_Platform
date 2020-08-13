# encoding: utf-8
"""
@auth: cyq
@name: tasks
@desc: tasks
"""
import time

from App import create_celery_app
from Model.Models import UICase
from comments.driverOpt import DriverOpt

celery = create_celery_app()



@celery.task
def runCase(caseId):
    case = UICase.get(caseId)
    info = {"caseId": case.id, "name": case.name, "desc": case.desc,
            "creator": case.creator,
            "headless": case.headless, "windowsSize": case.windowsSize,
            "status": case.status, "state": case.state,
            "steps": [{"stepId": s.id, "name": s.name, "desc": s.desc, "methodId": s.is_method, "type": s.type,
                       "locator": s.locator,
                       "do": s.do, "value": s.value, "variable": s.variable, "validate": s.validate} for
                      s in case.casesteps]}
    driver = DriverOpt(headless=info['headless'])
    driver.run(info["steps"])
