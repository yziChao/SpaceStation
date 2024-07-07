$(document).ready(function() {

  // Asignar placeholders para ayudar a los usuarios
  $('#id_username').attr('placeholder', 'Ej: Space');
  $('#id_password').attr('placeholder', 'Station');

  $('#form-ingreso').validate({ 
      rules: {
        'username': {
          required: true,
        },
        'password': {
          required: true,
        },
      },
      messages: {
        'username': {
          required: 'Debe ingresar un nombre de usuario',
        },
        'password': {
          required: 'Debe ingresar una contraseña',
        },
      },
      errorPlacement: function(error, element) {
        error.insertAfter(element); // Inserta el mensaje de error después del elemento
        error.addClass('invalid-feedback'); // Aplica una clase al mensaje de error
      },
  });

});
