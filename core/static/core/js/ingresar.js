$(document).ready(function() {

  // Asignar placeholders para ayudar a los usuarios
  $('#id_username').attr('placeholder', 'Ej: ziyuan, triveros, mgranifo, SpaceStation');
  $('#id_password').attr('placeholder', 'Ingresa tu contraseña actual');

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
          required: 'Debe ingresar un nombre de usuario.',
        },
        'password': {
          required: 'Debe ingresar una contraseña.',
        },
      },
      errorElement: 'div', // Utiliza un elemento <div> para los mensajes de error
      errorClass: 'invalid-feedback', // Aplica la clase de Bootstrap para los mensajes de error
      errorPlacement: function(error, element) {
          error.appendTo(element.parent()); // Inserta el mensaje de error después del elemento padre
      },
      highlight: function(element, errorClass, validClass) {
          $(element).addClass('is-invalid'); // Aplica la clase de Bootstrap para resaltar errores
      },
      unhighlight: function(element, errorClass, validClass) {
          $(element).removeClass('is-invalid'); // Quita la clase de Bootstrap cuando se corrige el error
      }
  });

  $('#user-select').change(function() {
    var username = $(this).val();
    var password = 'Duoc@123';
    if ('cevans eolsen tholland sjohansson cpratt mruffalo super'.includes(username)) {
      password = '123';
    };
    $('#id_username').val(username);
    $('#id_password').val(password);
  });

});
