odoo.define('mx_integritas_localizacion_cp.website_codigo', function (require) {
    'use strict';
    var sAnimations = require('website.content.snippets.animation');
    var core = require('web.core');
    var _t = core._t;

   

    sAnimations.registry.website_codigo = sAnimations.Class.extend({
        selector: '.div_zip input[name="zip"]',
        read_events: {
            'keyup': '_onGetCP',
        },

        /**
         * @override
         */
        start: function () {
            console.log("Active C.P. Integritas")
            var select = $("select[name='mx_integritas_colonia']")
            var input = $("input[name='l10n_mx_edi_colony']")
            if(select.val()==""|| select.val()==null){
                select.css("display","none")
                input.css("display","block")
            }else{
                select.css("display","block")
                input.css("display","none")
            }
            
            return null;
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         * @param {Event} ev
         */
        _onGetCP: function (ev) {
           var $codigo = $(ev.currentTarget).val()
            if($codigo!=""&&$codigo!=null&&$codigo.length>=5){
                var select = $("select[name='mx_integritas_colonia']")
                var input = $("input[name='l10n_mx_edi_colony']")
                
                $.ajax({
                    url: "https://api-sepomex.hckdrk.mx/query/info_cp/"+$codigo,
                    cache: false,
                    success: function(html){
                        select.val("").html("")
                        $("#mx_integritas_colonia").html("")
                        for(let index in html){
                            html[index].asentamiento;
                            var asentamiento = html[index].response.asentamiento;
                            $("#mx_integritas_colonia").append(`<option value="`+asentamiento+`">`+asentamiento+`</option>`)
                        }
                        $("input[name='l10n_mx_edi_colony']").val($("#mx_integritas_colonia").val())
                        var response = html[0].response
                        
                        $("input[name='city']").val(response.municipio)
                        $("select[name ='country_id'] > option").each(function() {
                        
                            if(this.text.toUpperCase() == response.pais.toUpperCase()){
                                var country = this.value;
                                $("select[name ='country_id']").on('change', function(){
                                    $("select[name ='country_id']").val(country)

                                });
                                
                                $("select[name ='country_id']").trigger('change')
                                setTimeout(function(){
                                    var _exist__ = 0;
                                    $("select[name ='state_id'] > option").each(function() {
                                        if(this.text.toUpperCase() == response.estado.toUpperCase()){
                                            $("select[name ='state_id']").val(this.value)
                                            _exist__ = 1;
                                        }
                                    });
                                    if(_exist__ == 0){
                                        $("select[name ='state_id'] > option").each(function() {
                                            if(response.estado.toUpperCase().indexOf(this.text.toUpperCase())!=-1){
                                                $("select[name ='state_id']").val(this.value)
                                            }
                                        });
                                    }
                                },1300)
                            }
                        });
                        if(select.val()==""|| select.val()==null){
                            select.css("display","none")
                            input.css("display","block")
                        }else{
                            select.css("display","block")
                            input.css("display","none")
                        }
                        
                    },error: function (request, status, error) {
                        select.val("").html("")
                        $("select[name ='state_id']").val("")
                        $("select[name ='country_id']").val("")
                        $("input[name='city']").val("")
                        if(select.val()==""|| select.val()==null){
                            select.css("display","none")
                            input.css("display","block")
                        }else{
                            select.css("display","block")
                            input.css("display","none")
                        }
                    }
                });
                
            }
 
        },
        
    });
});