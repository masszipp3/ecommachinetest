$('#title').on('input', function () {
    var title = $(this).val();
    var slug = '';
    slug = title.toLowerCase().replace(/\s+/g, '-');
    slug = slug.replace(/[^\w-]+/g, '');
    $('#slug').val(slug);
});