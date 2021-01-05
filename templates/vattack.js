<script type="text/javascript">
    function show_plot() {
	console.log(">>>>>>>> {{ is_grouped }}");
	var can_group = false;
	var searchtext = $('#searchtext').val();
	console.log(searchtext)
	if ( "{{ is_grouped }}" == "False" )
	{
	    can_group = true;
	}
	$.ajax({
	    url: "{{ url_for('plot') }}",
	    data: {
		can_group: can_group,
		search_text: searchtext
	    }
	}).done(function (reply) {
	    $('#container').html(reply);
	});
    }
</script>
