jQuery(function ($){
    jQuery.noConflict();
    $(document).ready(function(){
        $("#login").click(function(){
            jQuery.noConflict();
            $("#myModal").modal();
        });
        $("#logout").click(function(){
            logout_to_user();
        });

        show_contenidos();


    function show_contenidos(){
        if($(".login_on").length > 0){
            $(".contenidos").show();
        }
        else{
            console.log("hide");
            $(".contenidos").hide();
        }
    }


    function logout_to_user(){
        $.ajax({
                  url : '/',
                  type : "POST",
                  dataType : "json",
                  data : {'csrfmiddlewaretoken': csrftoken, 'logout':'1'},

                  success : function(data){
                    if(data.readyState==4 && data.status==200){
                        window.location.replace("/");
                    }
                  },
                  error : function(data){
                    if(data.readyState==4 && data.status==200){
                       window.location.replace("/");
                    }
                  }
              });
    }

    function login_to_user(){
        var uname = document.getElementById('id_username');
        var pass = document.getElementById('id_pass');
      $.ajax({
                  url : '/',
                  type : "POST",
                  dataType : "json",
                  data : {'csrfmiddlewaretoken': 'aqui', 'uname':uname,'pass':pass},

                  success : function(data){
                    console.log(data.username);

                  },
                  error : function(data){alert(data.response);}
              });

            }
        });
});