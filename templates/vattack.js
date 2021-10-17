<script type="text/javascript">
    function show_plot() {
	var can_group = true;
	var searchtext = $('#searchtext').val();
	console.log(searchtext)
	$('#container').html('Reticulating splines...');
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
