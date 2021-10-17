<script type="text/javascript">
    function show_plot(is_software_visible, is_groups_visible) {
	if ( is_software_visible == null )
	    is_software_visible = "False";
	if ( is_groups_visible == null )
	    is_groups_visible = "False";
	
	var can_group = true;
	var searchtext = $('#searchtext').val()
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
		search_text: searchtext,
		is_groups_visible: is_groups_visible,
		is_software_visible: is_software_visible
	    }
	}).done(function (reply) {
	    $('#container').html(reply);
	});
    }
</script>
