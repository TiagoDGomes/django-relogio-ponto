

(function(window, $) {
	$(document).ready(function(){
		var a = document.createElement('a');
		a.setAttribute('href','../../../colaboradores');
		a.innerHTML = 'Importar/Exportar';
		var li = document.createElement('li');		
		li.append(a);		
		$('.model-colaborador.change-list .object-tools').append(li);
	});
	
})(window, django.jQuery);