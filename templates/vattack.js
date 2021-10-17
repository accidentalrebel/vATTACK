<script type="text/javascript">
    function show_plot(software) {
	console.log("### 1 Show_plot(software) == " + software)
	if ( software == null )
	{
	    software = "False";
	}
	console.log("### 2 Show_plot(software) == " + software)
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
		is_software_visible: software
	    }
	}).done(function (reply) {
	    $('#container').html(reply);
	});
    }
</script>
