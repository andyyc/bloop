from django.http import HttpResponse
from django.templatetags.static import static
import json

def teams(request):
    response_data = {
        "ARI":static("team_icons/ARI.png"),
        "ATL":static("team_icons/ATL.png"),
        "BAL":static("team_icons/BAL.png"),
        "BUF":static("team_icons/BUF.png"),
        "CAR":static("team_icons/CAR.png"),
        "CHI":static("team_icons/CHI.png"),
        "CIN":static("team_icons/CIN.png"),
        "CLE":static("team_icons/CLE.png"),
        "DAL":static("team_icons/DAL.png"),
        "DEN":static("team_icons/DEN.png"),
        "DET":static("team_icons/DET.png"),
        "GB":static("team_icons/GB.png"),
        "HOU":static("team_icons/HOU.png"),
        "IND":static("team_icons/IND.png"),
        "JAC":static("team_icons/JAC.png"),
        "KC":static("team_icons/KC.png"),
        "MIA":static("team_icons/MIA.png"),
        "MIN":static("team_icons/MIN.png"),
        "NE":static("team_icons/NE.png"),
        "NO":static("team_icons/NO.png"),
        "NYG":static("team_icons/NYG.png"),
        "NYJ":static("team_icons/NYJ.png"),
        "OAK":static("team_icons/OAK.png"),
        "PHI":static("team_icons/PHI.png"),
        "PIT":static("team_icons/PIT.png"),
        "SD":static("team_icons/SD.png"),
        "SEA":static("team_icons/SEA.png"),
        "SF":static("team_icons/SF.png"),
        "STL":static("team_icons/STL.png"),
        "TB":static("team_icons/TB.png"),
        "TEN":static("team_icons/TEN.png"),
        "WAS":static("team_icons/WAS.png"),
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")
