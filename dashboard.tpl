<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>AMMD - Another minimal Minecraft Dashboard</title>

    <!-- Bootstrap -->
    <link href="resources/css/bootstrap.min.css" rel="stylesheet">
    <!-- Style -->
    <link href="resources/css/bootstrap-theme.min.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body role="document">


    <div class="container theme-showcase" role="main">


      <div class="page-header">
        <h1>AMMD <small>another minimal Minecraft Dashboard</small></h1>
      </div>

      <div class="row">
        <div class="col-sm-4">
          <div class="panel panel-default">
            <div class="panel-heading">
              <h3 class="panel-title">Server Status</h3>

            </div>
            

            <ul class="list-group">
              <li class="list-group-item">
                <p>CPU: {{stats["CPU"]}}%</p>
                
                <div class="progress">
                  <div class="progress-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" style="width: {{stats["CPU"]}}%;">
                  </div>
                </div>
              </li>

              <li class="list-group-item">
              <p>RAM: {{stats["RAM"][1]}}B / {{stats["RAM"][2]}}B</p>

                <div class="progress">
                  <div class="progress-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" style="width: {{stats["RAM"][0]}}%;">
                  </div>
                </div>

              </li>

              <li class="list-group-item">
              <p>SSD: {{stats["Disk"][1]}}B / {{stats["Disk"][2]}}B</p>

                <div class="progress">
                  <div class="progress-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" style="width: {{stats["Disk"][0]}}%;">
                  </div>
                </div>

              </li>
            </ul>
          </div>
        </div>

        <div class="col-sm-4">
          <div class="panel panel-default">
            <div class="panel-heading">
              <h3 class="panel-title">Minecraft
                % if stats["online"] == "online":
                <span class="label label-success pull-right">Online</span>
                % elif stats["online"] == "offline":
                <span class="label label-danger pull-right">Offline</span>
                % elif stats["online"] == "starting":
                <span class="label label-info pull-right">Starting...</span>
                % elif stats["online"] == "stopping":
                <span class="label label-warning pull-right">Stopping...</span>
                % end
              </h3>
            </div>

            <ul class="list-group">
              <li class="list-group-item">
                <form name="reply" id="replyForm" action="action" method = "POST">
                  <div class="btn-group btn-group-justified" role="group" aria-label="">
                    <div class="btn-group" role="group">
                      <button id="ServerActionStart" type="submit" class="btn btn-default" value="start">Start</button>
                    </div>  
                    <div class="btn-group" role="group">
                      <button id="ServerActionStop" type="submit" class="btn btn-default" value="stop">Stop</button>
                    </div>
                    <div class="btn-group" role="group">
                      <button id="ServerActionKill" type="submit" class="btn btn-default" value="kill">Kill</button>
                    </div>
                  </div>
                </form>
              </li>

              % if stats["online"] == "online":
              <li class="list-group-item">
                <p><b>Players online:</b> {{stats["players"]}}</p>
              </li>

              <li class="list-group-item">
                <p><b>Latency:</b> {{stats["latency"]}}ms</p>
              </li>

              % else:

              <li class="list-group-item">
                <b>Server offline</b>
              </li>

              % end
            </ul>

          </div>
        </div>

        <div class="col-sm-4">
          <div class="panel panel-default">
            <div class="panel-heading">
              <h3 class="panel-title">Log</h3>
            </div>
          

          
            <ul class="list-group">
              % for entry in stats["log"]:
                <li class="list-group-item">
                  <p>{{entry}}</p>
                </li>
              % end
            </ul>
          </div>
        </div>

      </div>
    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>

    <script>
      $(function(){
        $('#ServerActionStart, #ServerActionStop, #ServerActionKill').on('click', function(e){
          e.preventDefault(); // preventing default click action
          type = $(this).attr("value");
          if (type=="stop" || type=="kill"){
            if(!confirm("Do you really want to "+type+" the server?")){
              return
            }
          }
          $.ajax({

            url: '/action',
            type: 'post',
            data: JSON.stringify({action: $(this).attr("value")}),
            contentType: 'application/json;charset=UTF-8',
            success: function (response) {
              location.reload();
              // ajax success callback
            }, error: function (response) {
              alert(response);
              // ajax error callback
            },
          });
        });
      });
    </script>

    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="resources/js/bootstrap.min.js"></script>
  </body>
</html>