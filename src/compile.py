
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize



ext_modules = [

    #   ... all your modules that need be compiled ...
    Extension("AllStrings",  					[".\src\AllStrings.py"]),
    ###Extension("AutoCaptureFaceForTraining", 	[".\src\AutoCaptureFaceForTraining.py"]),
    Extension("common_fun",  					[".\src\common_fun.py"]),
    Extension("Mongo_DB",  						[".\src\Mongo_DB.py"]),
    Extension("PageChangePW",  					[".\src\PageChangePW.py"]),
    Extension("PageForgotPW",  					[".\src\PageForgotPW.py"]),
    Extension("PageHome",  						[".\src\PageHome.py"]),
    Extension("PageTrialNag",  					[".\src\PageTrialNag.py"]),
    Extension("Page_About",  					[".\src\Page_About.py"]),
    Extension("Page_AddRecord",  				[".\src\Page_AddRecord.py"]),
    Extension("Page_AttendanceSystem",  		[".\src\Page_AttendanceSystem.py"]),
    
    Extension("Page_FaceRecognition",  			[".\src\Page_FaceRecognition.py"]),
    Extension("Page_Login",  					[".\src\Page_Login.py"]),
    Extension("Page_RegisterNewUser",  			[".\src\Page_RegisterNewUser.py"]),
    Extension("Page_RemoveFaceFrom_Detection",	[".\src\Page_RemoveFaceFrom_Detection.py"]),
    Extension("Page_TrainedSystem",  			[".\src\Page_TrainedSystem.py"]),
    Extension("Page_YearWiseAttendance",  		[".\src\Page_YearWiseAttendance.py"]),
    Extension("StartSystemImageTraining",  		[".\src\StartSystemImageTraining.py"]),
    Extension("Start_Stop_MongoDb",  			[".\src\Start_Stop_MongoDb.py"]),
    Extension("TakeEmpPhotoPage",  				[".\src\TakeEmpPhotoPage.py"]),

    Extension("Page_EditRecord",  				[".\src\Page_EditRecord.py"]),

]


setup(
    name = 'MyFR_Program_Name',
    cmdclass = {'build_ext': build_ext},
    ##ext_modules = ext_modules
    ext_modules = cythonize(  ext_modules )

)