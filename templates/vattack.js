<script type="text/javascript">
    function show_plot(is_tools_visible, is_groups_visible, is_mitigations_visible, is_malware_visible) {
	if ( is_tools_visible == null )
	    is_tools_visible = "False";
 	if ( is_groups_visible == null )
	    is_groups_visible = "False";
	if ( is_mitigations_visible == null )
	    is_mitigations_visible = "False";
	if ( is_malware_visible == null )
	    is_malware_visible = "False";
	
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
		is_mitigations_visible: is_mitigations_visible,
		is_malware_visible: is_malware_visible,
		is_tools_visible: is_tools_visible
	    }
	}).done(function (reply) {
	    $('#container').html(reply);
	});
    }
</script>
