$(document).ready(function() {

  // Asignar placeholders para ayudar a los usuarios
  $('#id_username').attr('placeholder', 'Ej: cgomezv, cevans, sjohasson');
  $('#id_first_name').attr('placeholder', 'Ej: Cristián, Chris, Scarlett');
  $('#id_last_name').attr('placeholder', 'Ej: Gómez Vega, Evans, Johansson');
  $('#id_email').attr('placeholder', 'Ej: cevans@marvels.com');
  $('#id_rut').attr('placeholder', 'Ej: 11111111-1 (sin puntos y con guión)');
  $('#id_direccion').attr('placeholder', 'Calle, n° casa o edificio, n° departamento o piso\n' +
    'localidad o ciudad, código postal o de área\n' +
    'estado o provincia, ciudad, país');

  // Agregar una validación por defecto para que la imagen la exija como campo obligatorio
  $.extend($.validator.messages, {
    required: "Este campo es requerido",
  });

  $("#mis-datos").validate({
    rules: {
      rut: {
        required: true,
        rutChileno: true
      },
      nombre: {
        required: true,
        soloLetras: true
      },
      apellido: {
        required: true,
        soloLetras: true
      },
      correo: {
        required: true,
        email: true, // Corregido: es 'email' en lugar de 'emailCompleto'
      },
      direccion: {
        required: true,
        minlength: 5, // Ejemplo: cambiar según tus requisitos
      },
      contraseña: {
        required: true,
        minlength: 5,
        maxlength: 15,
      },
      contraseña2: {
        required: true,
        equalTo: "#id_password", // Corregido: debe coincidir con el campo de contraseña original
        maxlength: 15,
      },
    },
    messages: {
      rut: {
        required: "El rut es un campo obligatorio",
        rutChileno: "El formato del rut no es válido"
      },
      nombre: {
        required: "El nombre es un campo obligatorio",
      },
      apellido: {
        required: "El apellido es un campo obligatorio",
      },
      correo: {
        required: "El email es un campo requerido",
        email: "El email no cumple el formato de un correo",
      },
      direccion: {
        required: "La dirección es un campo requerido",
        minlength: "La dirección debe tener al menos {4} caracteres",
      contraseña: {
        required: "La contraseña es un campo requerido",
        minlength: "La contraseña debe tener un mínimo de {0} caracteres",
        maxlength: "La contraseña debe tener un máximo de {4} caracteres",
      },
      contraseña2: {
        required: "Repetir contraseña es un campo requerido",
        equalTo: "Debe repetir la contraseña escrita anteriormente",
      },
    },
    errorPlacement: function(error, element) {
      error.insertAfter(element); // Inserta el mensaje de error después del elemento
      error.addClass('error-message'); // Aplica una clase al mensaje de error
    },
}});

});
