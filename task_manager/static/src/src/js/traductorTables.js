window.onload = function() {
    var Tablas = document.getElementsByTagName("table");
    for (var t=0; t<Tablas.length; t++){
        var nombreTabla=Tablas[t].id, wrapper = nombreTabla+'_wrapper', length = nombreTabla+'_length', 
        filter = nombreTabla+'_filter', info = nombreTabla+'_info', paginate = nombreTabla+'_paginate'
        $('#'+wrapper).addClass("justify-content-between");

        $('#'+length+' label').addClass("row align-items-center");
        $('#'+length).addClass("col-md-2");        
        var eleLength = document.getElementById(length); 
        if(eleLength!=null){
            try {                
                if (eleLength.children.length>0){
                    var label = eleLength.children[0]
                    label.childNodes[0].nodeValue = '';
                    label.childNodes[2].nodeValue = '';
                }
            }catch (error) {   }
        }
        
        $('#'+length+' label select').addClass("form-control");
        
        $('#'+length+' label select option[value="10"]').text('Mostrando 10');
        $('#'+length+' label select option[value="25"]').text('Mostrando 25');
        $('#'+length+' label select option[value="50"]').text('Mostrando 50');
        $('#'+length+' label select option[value="100"]').text('Mostrando 100');

        $('#'+filter).addClass("col-md-4"); 
        var eleFilter = document.getElementById(filter);         
        if(eleFilter!=null){
            try {
                if (eleFilter.children.length>0){
                    var label = eleFilter.children[0]
                    label.childNodes[0].nodeValue = '';
                }
            }catch (error) {   }
        }
        $('#'+filter+' label').addClass("w-100");
        $('#'+filter+' input').addClass("form-control w-100");
        $('#'+filter+' input').attr('placeholder', 'Buscador..');    

        let i = 0;
        while (i == 0) {
            console.log( $('#'+nombreTabla+'_previous') ) 
            if ($('#'+nombreTabla+'_previous')){
                if($('#'+nombreTabla+'_previous').length>0) {
                    $('#'+nombreTabla+'_previous').text("Anterior");
                    i=1;
                // }else{
                //     console.log("else 2");
                //     setInterval(function() {
                //         i = 0 
                //     }, 500)
                }
            // }else{
            //     console.log("else 1");
            //     setInterval(function() {
            //         i = 0 
            //     }, 500)
            }
        }
        
    }
        
    // console.log($('#visitantes_previous'))
    // $('#visitantes_previous').text("Anterior");
    // console.log($('#visitantes_next'))
    // $('#visitantes_next').text("Siguiente");

    // var visitantes_info = $('#visitantes_info');
    // visitantes_info.on('click', function() { 
    //     console.log("Cambio algo")
    //     var textoEnEspanol = traducirTexto( visitantes_info.val() );
    // });
}