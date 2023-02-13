const customToolbar = [
    {
        name: 'bold',
        action: (editor) => {
            editor.toggleBold()
        },
        className: 'fa fa-bold',
        title: 'Gras'
    },
    {
        name: 'italic',
        action: (editor) => {
            editor.toggleItalic()
        },
        className: 'fa fa-italic',
        title: 'Italic'
    },
    {
        name: 'heading',
        action: (editor) => {
            editor.toggleHeadingSmaller()
        },
        className: 'fa fa-header',
        title: 'Titre'
    },
    '|',
    {
        name: 'quote',
        action: (editor) => {
            editor.toggleBlockquote()
        },
        className: 'fa fa-quote-left',
        title: 'Citation'
    },
    {
        name: 'ordered-list',
        action: (editor) => {
            editor.toggleOrderedList()
        },
        className: 'fa fa-list-ol',
        title: 'Liste ordonnée'
    },
    {
        name: 'unordered-list',
        action: (editor) => {
            editor.toggleUnorderedList()
        },
        className: 'fa fa-list-ul',
        title: 'Liste à puces'
    },
    '|',
    {
        name: 'heading-smaller',
        action: (editor) => {
            editor.toggleHeadingSmaller()
        },
        className: 'fa fa-header',
        title: 'Titre plus petit'
    },
    {
        name: 'heading-bigger',
        action: (editor) => {
            editor.toggleHeadingBigger()
        },
        className: 'fa fa-lg fa-header',
        title: 'Titre plus grand'
    },
    '|',
    {
        name: 'link',
        action: (editor) => {
            editor.drawLink()
        },
        className: 'fa fa-link',
        title: 'Insérer un lien'
    },
    {
        name: 'image',
        action: (editor) => {
            editor.drawImage()
        },
        className: 'fa fa-picture-o',
        title: 'Insérer un image'
    },
    {
        name: 'table',
        action: (editor) => {
            editor.drawTable()
        },
        className: 'fa fa-table',
        title: 'Insérer un tableau'
    },
    '|',
    {
        name: 'preview',
        action: (editor) => {
            editor.togglePreview()
            document.querySelectorAll('.editor-preview').forEach(el => { el.classList.add('content'); console.log('t') })
        },
        className: 'fa fa-eye no-disable',
        title: 'Aperçu'
    },
    {
        name: 'side-by-side',
        action: (editor) => {
            editor.toggleSideBySide()
            document.querySelectorAll('.editor-preview-side').forEach(el => { el.classList.add('content') })
        },
        className: 'fa fa-columns no-disable no-mobile',
        title: 'Édition côte à côte'
    },
    {
        name: 'fullscreen',
        action: (editor) => {
            editor.toggleFullScreen()
        },
        className: 'fa fa-expand no-disable no-mobile',
        title: 'Plein écran'
    },
    '|',
    {
        name: 'add-section',
        action: (editor) => {
            editor.value(editor.value() + "\n\n%section%\n\n")
        },
        className: "fas fa-layer-plus",
        title: 'Ajouter une section'
    },
    {
        name: 'next-step-requirements',
        action: (editor) => {
            editor.value(editor.value() + "\n%suite%\n\n* Ce point doit être respecté pour passer à la suite\n* Celui ci aussi\n\n%suite-fin%")
        },
        className: "fas fa-comment-exclamation",
        title: 'Points à respecter pour passer à l\'étape suivante'
    }
]
