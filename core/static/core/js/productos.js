$(document).ready(function() {

    // Cambiar el texto del combo de categoría por "Seleccione una categoría"
    var select = document.querySelector('select[name="categoria"]');
    if (select) {
        var defaultOption = select.querySelector('option[value=""]');
        if (defaultOption) {
            defaultOption.text = "Seleccione una categoría";
        }
    }

    // Asignar placeholders para ayudar a los usuarios
    $('#id_nombre').attr('placeholder', 'Ej: Diablo 4, Uncharted 2, God of War 2');
    $('#id_descripcion').attr('placeholder', 'Ej: Diablo IV es un juego de rol de acción de mazmorras desarrollado y publicado por Blizzard Entertainment.');
    $('#id_precio').attr('placeholder', 'Ej: 35000');
    $('#id_descuento_subscriptor').attr('placeholder', 'Ej: 10');
    $('#id_descuento_oferta').attr('placeholder', 'Ej: 5');

    // Agregar una validación por defecto para que la imagen la exija como campo obligatorio
    $.extend($.validator.messages, {
        required: "Este campo es requerido",
    });

    // Agregar validación para que la suma de los descuentos no supere el 100%
    $.validator.addMethod('sumaDescuentos', function(value, element) {
        
        var descuentoSubscriptor = parseFloat($('#id_descuento_subscriptor').val());
        var descuentoOferta = parseFloat($('#id_descuento_oferta').val());
        var sumaDescuentos = descuentoSubscriptor + descuentoOferta;
        
        if (isNaN(descuentoSubscriptor) || isNaN(descuentoOferta)) return true;

        return sumaDescuentos <= 100;

    }, 'La suma de los descuentos no puede superar el 100%');

    $('#form').validate({ 
        rules: {
            'categoria': {
                required: true,
            },
            'nombre': {
                required: true,
            },
            'descripcion': {
                required: true,
            },
            'precio': {
                required: true,
                digits: true,
                number: true,
            },
            'descuento_subscriptor': {
                required: true,
                digits: true,
                number: true,
                range: [0, 100],
                sumaDescuentos: true,
            },
            'descuento_oferta': {
                required: true,
                digits: true,
                number: true,
                range: [0, 100],
                sumaDescuentos: true,
            },
        },
        messages: {
            'categoria': {
                required: 'Debe ingresar la categoría del producto',
            },
            'nombre': {
                required: 'Debe ingresar el nombre del producto',
            },
            'descripcion': {
                required: 'Debe ingresar la descripción del producto',
            },
            'precio': {
                required: 'Debe ingresar el precio del producto',
                number: 'Debe ingresar un número',
                digits: 'Debe ingresar un número entero',
            },
            'descuento_subscriptor': {
                required: 'Debe ingresar el % de descuento para subscriptores',
                number: 'Debe ingresar un número',
                digits: 'Debe ingresar un número entero',
                range: 'El descuento debe ser un número entre 0 y 100',
            },
            'descuento_oferta': {
                required: 'Debe ingresar el % de descuento para ofertas',
                number: 'Debe ingresar un número',
                digits: 'Debe ingresar un número entero',
                range: 'El descuento debe ser un número entre 0 y 100',
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

});
