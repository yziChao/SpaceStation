$(document).ready(function() {

  // Asignar placeholders para ayudar a los usuarios
  $('#id_username').attr('placeholder', 'Ej: SpaceStation');
  $('#id_first_name').attr('placeholder', 'Ej: Space');
  $('#id_last_name').attr('placeholder', 'Ej: Station');
  $('#id_email').attr('placeholder', 'Ej: spacestation@ss.com');
  $('#id_password1').attr('placeholder', '8 caracteres como mínimo');
  $('#id_password2').attr('placeholder', 'Repetir la contraseña escogida');
  $('#id_rut').attr('placeholder', 'Ej: 11111111-1 (sin puntos y con guión)');
  $('#id_direccion').attr('placeholder', 'Calle, n° casa o edificio, n° departamento o piso\n'
    + 'localidad o ciudad, código postal o de área\n'
    + 'estado o provincia, ciudad, país');

  // Agregar una validación por defecto para que la imagen la exija como campo obligatorio
  $.extend($.validator.messages, {
    required: "Este campo es requerido",
  });

  $('#form-registrarme').validate({ 
      rules: {
        'username': {
          required: true,
        },
        'first_name': {
          required: true,
          soloLetras: true,
        },
        'last_name': {
          required: true,
          soloLetras: true,
        },
        'email': {
          required: true,
          emailCompleto: true,
        },
        'rut': {
          required: true,
          rutChileno: true,
        },
        'direccion': {
          required: true,
        },
        'password1': {
          required: true,
          minlength: 8,
        },
        'password2': {
          required: true,
          equalTo: '#id_password1'
        }
      },
      messages: {
        'username': {
          required: 'Debe ingresar un nombre de usuario',
        },
        'first_name': {
          required: 'Debe ingresar su nombre',
          soloLetras: "El nombre sólo puede contener letras y espacios en blanco",
        },
        'last_name': {
          required: 'Debe ingresar sus apellidos',
          soloLetras: "Los apellidos sólo pueden contener letras y espacios en blanco",
        },
        'email': {
          required: 'Debe ingresar su correo',
          emailCompleto: 'El formato del correo no es válido',
        },
        'rut': {
          required: 'Debe ingresar su RUT',
          rutChileno: 'El formato del RUT no es válido',
        },
        'direccion': {
          required: 'Debe ingresar su dirección',
        },
        'password1': {
          required: 'Debe ingresar una contraseña',
          minlength: 'La contraseña debe tener al menos 8 caracteres',
        },
        'password2': {
          required: 'Debe ingresar una contraseña',
          equalTo: 'Debe repetir la contraseña anterior'
        }
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

});
