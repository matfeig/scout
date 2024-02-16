import os 
import pandas as pd
# chemin utilitaire
PATH = os.getcwd()
PATH_MODEL = os.getcwd() + "/models/"
PATH_CLOUD = os.getcwd() + "/application/cloud_storage/projetcloudangeloz-1d127b662e44.json"

database = pd.read_csv(
            os.getcwd() + "/application/data/ressources/database_complete.csv",
            header=0,
            sep=",",
        )

# colonnes ["numéro de la colonne" , "nom de la colonne originale"]
class Cols:
    NAME = [0, "Name"]
    PLAYER_ID = [1, "Player ID"]
    NUMBER = [2, "Number"]
    GROUPEID = [3, "Group Id"]
    GROUPENAME = [4, "Group name"]
    LEAGUEID = [5, "League ID"]
    TIME = [6, "Time (s)"]
    TIMEFILED = [7, "Time on Playing Field (s)"]
    DISTANCE = [8, "Distance (m)"]
    STEPS = [9, "Steps"]
    TIMESPEEDVLOW = [10, "Time (speed | Very low) (s)"]
    TIMESPEEDLOW = [11, "Time (speed | Low) (s)"]
    TIMESPEEDMEDIUM = [12, "Time (speed | Medium) (s)"]
    TIMESPEEDHIGH = [13, "Time (speed | High) (s)"]
    TIMESPEEDVHIGH = [14, "Time (speed | Very high) (s)"]
    DISTANCESPEEDVLOW = [15, "Distance (speed | Very low) (m)"]
    DISTANCESPEEDLOW = [16, "Distance (speed | Low) (m)"]
    DISTANCESPEEDMEDIUM = [17, "Distance (speed | Medium) (m)"]
    DISTANCESPEEDHIGH = [18, "Distance (speed | High) (m)"]
    DISTANCESPEEDVHIGH = [19, "Distance (speed | Very high) (m)"]
    JUMPS = [20, "Jumps"]
    FCRECUP = [21, "Heart Rate Recoveries"]
    IMPACT = [22, "Impacts"]
    ACCEL = [23, "Accelerations"]
    ACCELMIN = [24, "Accelerations / min"]
    DECEL = [25, "Decelerations"]
    DECELMIN = [26, "Decelerations / min"]
    SPRINT = [27, "Sprints"]
    JUMPLOW = [28, "Jumps (Low)"]
    JUMPMEDIUM = [29, "Jumps (Medium)"]
    JUMPHIGH = [30, "Jumps (High)"]
    JUMPVHIGH = [31, "Jumps (Very high)"]
    CODS = [32, "Changes of Direction"]
    CODSLEFT = [33, "Changes of Direction (left)"]
    CODSRIGHT = [34, "Changes of Direction (right)"]
    ACCELLOW = [35, "Accelerations (Low)"]
    ACCELMEDIUM = [36, "Accelerations (Medium)"]
    ACCELHIGH = [37, "Accelerations (High)"]
    ACCELVHIGH = [38, "Accelerations (Very high)"]
    DECELLOW = [39, "Decelerations (Low)"]
    DECELMEDIUM = [40, "Decelerations (Medium)"]
    DECELHIGH = [41, "Decelerations (High)"]
    DECELVHIGH = [42, "Decelerations (Very high)"]
    SPRINTLOW = [43, "Sprints (Low)"]
    SPRINTMEDIUM = [44, "Sprints (Medium)"]
    SPRINTHIGH = [45, "Sprints (High)"]
    SPRINTCHIGH = [46, "Sprints (Very high)"]
    JUMPLOAD = [47, "Jump Load (J)"]
    JUMPLOADKG = [48, "Jump Load per mass (J/kg)"]
    JUMPLOADMIN = [49, "Jump Load / min (J)"]
    JUMPLOADKGMIN = [50, "Jump Load per mass / min (J/kg)"]
    FCMOY = [51, "Heart Rate (Ø) (bpm)"]
    FCMAX = [52, "Heart Rate (max.) (bpm)"]
    FCMIN = [53, "Heart Rate (min.) (bpm)"]
    TRIMP = [54, "TRIMP"]
    ACCELLOADMIN = [55, "Acceleration Load / min"]
    ACCUMACCELLOAD = [56, "Accumulated Acceleration Load"]
    ACCUMACCELLOADMIN = [57, "Accumulated Acceleration Load / min"]
    METAPOWERMAX = [58, "Metabolic Power (max.) (W)"]
    METAPOWERKG = [59, "Metabolic Power per mass (max.) (W/kg)"]
    METAPOWER = [60, "Metabolic Power (Ø) (W)"]
    METAPOWERKG = [61, "Metabolic Power per mass (Ø) (W/kg)"]
    HIGHSPEEDACCELDISTANCE = [62, "High Speed and Acceleration Distance (m)"]
    HMPD = [63, "High Metabolic Power Distance (m)"]
    METAWORK = [64, "Metabolic Work (kcal)"]
    METAWORKMIN = [65, "Metabolic Work / min (kcal)"]
    TIMEFC050 = [66, "Heart Rate (time | 0 - 50%) (s)"]
    TIMEFC5060 = [67, "Heart Rate (time | 50 - 60%) (s)"]
    TIMEFC6070 = [68, "Heart Rate (time | 60 - 70%) (s)"]
    TIMEFC7080 = [69, "Heart Rate (time | 70 - 80%) (s)"]
    TIMEFC8090 = [70, "Heart Rate (time | 80 - 90%) (s)"]
    TIMEFCSUP90 = [71, "Heart Rate (time | ≥ 90%) (s)"]
    ACCELOADLOW = [72, "Acceleration Load (load | Low)"]
    ACCELLOADMEDIUM = [73, "Acceleration Load (load | Medium)"]
    ACCELLOADHIGH = [74, "Acceleration Load (load | High)"]
    ACCELLOADVHIGH = [75, "Acceleration Load (load | Very high)"]
    METAPOWERTIMELOW = [76, "Metabolic Power (time | Low) (s)"]
    METAPOWERTIMEMEDIUM = [77, "Metabolic Power (time | Medium) (s)"]
    METAPOWERTIMEHIGH = [78, "Metabolic Power (time | High) (s)"]
    METAPOWERTIMEVHIGH = [79, "Metabolic Power (time | Very high) (s)"]
    DATAQUALITY = [80, "Data Quality (%)"]
    DISTANCEMIN = [81, "Distance / min (m)"]
    VMAX = [82, "Speed (max.) (km/h)"]
    VMOY = [83, "Speed (Ø) (km/h)"]
    ACCMAX = [84, "Acceleration (max.) (m/s²)"]
    DECMAX = [85, "Deceleration (max.) (m/s²)"]
    POSTE = [86, "Position"]
    VITPOURCENTAGEMAX = [87, "Speed (% of max.) (%)"]
    HIGHSPEEDACCELTIME = [88, "High Speed and Acceleration Time (s)"]
    TEMPHUMANMAX = [89, "Human Core Temperature (max.) (°C)"]
    TEMPHUMANMOY = [90, "Human Core Temperature (Ø) (°C)"]
    ACCELMINLOW = [91, "Accelerations / min (Low)"]
    ACCELMINMEDIUM = [92, "Accelerations / min (Medium)"]
    ACCELMINHIGH = [93, "Accelerations / min (High)"]
    ACCELMINVHIGH = [94, "Accelerations / min (Very high)"]
    DECELMINLOW = [95, "Decelerations / min (Low)"]
    DECELMINMEDIUM = [96, "Decelerations / min (Medium)"]
    DECELMINHIGH = [97, "Decelerations / min (High)"]
    DECELMINVHIGH = [98, "Decelerations / min (Very high)"]
    CODSMIN = [99, "Changes of Direction / min"]
    IMPACTMIN = [100, "Impacts / min"]
    JUMPMIN = [101, "Jumps / min"]
    SPRINTMIN = [102, "Sprints / min"]
    TYPES = [103, "Types"]
    DESCRIPTION = [104, "Description"]
    SESSIONID = [105, "Session ID"]
    SES1 = [106, "Session begin (Local timezone)"]
    SES2 = [107, "Session begin (UTC)"]
    SES3 = [108, "Session begin date (Local timezone)"]
    DATE = [109, "Session begin date (UTC)"]
    SES5 = [110, "Session begin time (Local timezone)"]
    SES6 = [111, "Session begin time (UTC)"]
    SES7 = [112, "Session end (Local timezone)"]
    SES8 = [113, "Session end (UTC)"]
    SES9 = [114, "Session end date (Local timezone)"]
    SES10 = [115, "Session end date (UTC)"]
    SES11 = [116, "Session end time (Local timezone)"]
    SES12 = [117, "Session end time (UTC)"]
    EQUIPE = [118, "Equipe"]
    GROUPE = [119, "Groupe"]
    TYPESEANCE = [120, "Type_seance"]
    GLOBALLOAD = [121, "PlayerLoad"]

class VariablesUtils:

    LISTE_PLAYERS = ['Joueur 01', 'Joueur 02', 'Joueur 03', 'Joueur 04', 'Joueur 05', 'Joueur 06', 'Joueur 07', 'Joueur 08', 'Joueur 09', 'Joueur 10', 'Joueur 11', 'Joueur 12', 'Joueur 13', 'Joueur 14', 'Joueur 15', 'Joueur 16', 'Joueur 17', 'Joueur 18', 'Joueur 19', 'Joueur 20', 'Joueur 21', 'Joueur 22', 'Joueur 23', 'Joueur 24', 'Joueur 25', 'Joueur 26', 'Joueur 27', 'Joueur 28', 'Joueur 29', 'Joueur 30', 'Joueur 31', 'Joueur 32', 'Joueur 33']
    GENERATION = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007','']
    TEST_TYPE = ['F0', 'V0', 'VAMEVAL', 'VMI', 'TAILLE', 'POIDS', 'MG', 'TAILLE ASSISE', '5M', '10M', '30M', 'POSTURO', 'SJ', 'CMJ', 'CMJF','']
    INDICATEURS = ['Accumulated Acceleration Load', 'Distance (m)','Distance (speed | High) (m)', 'PlayerLoad']
    DICT_INDICATEURS_MONITORING = {'Distance':'Distance (m)', 'HID24':'Distance (speed | High) (m)', 'DistanceAcc':'Accumulated Acceleration Load', 'PlayerLoad' : 'PlayerLoad'}

    COLONNE_STR = database.select_dtypes('object').columns.values.tolist()
    COLONNE_FLOAT = database.select_dtypes('float64').columns.values.tolist()
    COLONNE_FIXE = ['Name','Player ID','Number','Group Id','Group name','League ID', 'Equipe']
    COLONNE_INDIC = list(set(COLONNE_FLOAT) - set(COLONNE_FIXE))
    COLONNE_DATE = ["Session begin (Local timezone)",
                    "Session begin (UTC)",
                    "Session begin date (Local timezone)",
                    "Session begin date (UTC)",
                    "Session begin time (Local timezone)",
                    "Session begin time (UTC)",
                    "Session end (Local timezone)",
                    "Session end (UTC)",
                    "Session end date (Local timezone)",
                    "Session end date (UTC)"
                    "Session end time (Local timezone)",
                    "Session end time (UTC)"]
    DICT_POSTES = {'Joueur 01': 'Left Wing', 'Joueur 02': 'Right Wing', 'Joueur 03': 'Right Back', 'Joueur 04': 'Left Back', 'Joueur 05': 'Right Wing', 'Joueur 06': 'Pivot', 'Joueur 07': 'Pivot', 'Joueur 08': 'Center', 'Joueur 09': 'Pivot', 'Joueur 10': 'Left Wing', 'Joueur 11': 'Right Back', 'Joueur 12': 'Center', 'Joueur 13': 'Center', 'Joueur 14': 'Goalkeeper', 'Joueur 15': 'Goalkeeper', 'Joueur 16': 'Center', 'Joueur 17': 'Pivot', 'Joueur 18': 'Left Back', 'Joueur 19': 'Right Wing', 'Joueur 20': 'Right Back', 'Joueur 21': 'Left Back', 'Joueur 22': 'Goalkeeper', 'Joueur 23': 'Pivot', 'Joueur 24': 'Goalkeeper', 'Joueur 25': 'Left Wing', 'Joueur 26': 'Right Back', 'Joueur 27': 'Left Wing', 'Joueur 28': 'Center', 'Joueur 29': 'Right Back', 'Joueur 30': 'Left Back', 'Joueur 31': 'Right Back', 'Joueur 32': 'Left Back', 'Joueur 33': 'Right Wing'}