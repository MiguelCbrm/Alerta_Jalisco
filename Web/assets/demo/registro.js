type = ['', 'info', 'success', 'warning', 'danger'];

registro = {
  initRegistro: function(){

    function authUser(user, pwd){
      var authenticationData = {
        Username : user,
        Password : pwd,
      };
      var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(authenticationData);
      var poolData = { UserPoolId : 'us-east-2_ZGkLooSXo',
          ClientId : 'c2v2u3nc4didc59saq5lo16jk'
      };
      var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
      var userData = {
          Username : user,
          Pool : userPool
      };
      var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
      
      cognitoUser.authenticateUser(authenticationDetails, {
          onSuccess: function (result) {
              var accessToken = result.getAccessToken().getJwtToken();
              
              /* Use the idToken for Logins Map when Federating User Pools with identity pools or when passing through an Authorization Header to an API Gateway Authorizer*/
              var idToken = result.idToken.jwtToken;
              localStorage.token = idToken;
              localStorage.user = user;
              cognitoUser = result.user;
              swal({
                position: 'top-end',
                title: 'Iniciando sesión...',
                showConfirmButton: false,
              }).catch(swal.noop);
              swal.showLoading();
              setTimeout( function(){ 
                loginUser();
              }  , 2000 );
            },
          onFailure: function(err) {
              alert(err);
          },
      });
    }

    function loginUser(){
      $.getJSON({
        url: "http://localhost:8080/myapp/verify/authUser/",
        headers: {"Authorization": localStorage.token},
        success: function(result){
          if(result == false){
            setTimeout( function(){ 
              loginUser();
            }  , 1000 );
          }
          else{
            window.location.replace('../../html_files_binasa/index_bin.html');
          }          
        }
      });
    }

    function registerUser(username, name, family_name, email, password){
      var poolData = { UserPoolId : 'us-east-2_vDxdSsB53',
        ClientId : '1kuk619hkhrggf1fvd2ns3p48a'
      };
      var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

      var attributeList = [];
      
      var dataName = {
        Name : 'name',
        Value : name
      };
      var dataFamilyName = {
        Name : 'family_name',
        Value : family_name
      };
      var dataEmail = {
        Name : 'email',
        Value : email
      };

    var attributeName = new AmazonCognitoIdentity.CognitoUserAttribute(dataName);
    var attributeFamilyName = new AmazonCognitoIdentity.CognitoUserAttribute(dataFamilyName);
    var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);

    attributeList.push(attributeName);
    attributeList.push(attributeFamilyName);
    attributeList.push(attributeEmail);

    userPool.signUp(username, password, attributeList, null, function(err, result){
        if (err) {
            alert(err);
            return;
        }
        cognitoUser = result.user;
        console.log('user name is ' + cognitoUser.getUsername());
    });
    }

    $("#button_registro").click(function() {
      var username = $('#input_username').val();
      var name = $('#input_name').val();
      var familyName = $('#input_familyName').val();
      var email = $('#input_email').val();
      var pwd = $('#input_password').val();
      registerUser(username, name, familyName, email, pwd);
    });

  },
};