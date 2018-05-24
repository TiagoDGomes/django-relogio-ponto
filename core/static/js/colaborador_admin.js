

(function(window, $) {
	$(document).ready(function(){
		var a = document.createElement('a');
		a.setAttribute('href','../../../colaboradores');
		a.innerHTML = 'Importar/Exportar';
		var li = document.createElement('li');		
		li.append(a);		
		$('.model-colaborador.change-list .object-tools').append(li);
		
		var aa = document.createElement('a');
		id = $('#id_matriculas-__prefix__-colaborador').val();
		aa.setAttribute('href','../../../../../batidas/' + id);
		aa.innerHTML = 'Batidas';
		var lia = document.createElement('li');
		lia.append(aa);		
		$('.model-colaborador.change-form .object-tools').append(lia);
		
	});
	
})(window, django.jQuery);