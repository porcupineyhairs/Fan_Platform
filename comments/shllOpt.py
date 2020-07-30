import subprocess
import allure

class Shell:
    @staticmethod
    def invoke(cmd):
        print("执行命令：", cmd)
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        return o


if __name__ == '__main__':
    # Shell.invoke("allure-2.9.0/bin/allure generate /home/mi/Fan_Platform/suite/tesInterfaces/allure_results -o  report --clean")
    Shell.invoke("allure-2.9.0/bin/allure serve /home/mi/Fan_Platform/suite/tesInterfaces/allure_results")
