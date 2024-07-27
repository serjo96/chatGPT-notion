from flask_restx import fields, Namespace

api = Namespace('blocks_models', description='Models for blocks related operations')

block_type_enum = [
    'bookmark', 'breadcrumb', 'bulleted_list_item', 'callout', 'child_database', 'child_page',
    'column', 'column_list', 'divider', 'embed', 'equation', 'file', 'heading_1',
    'heading_2', 'heading_3', 'image', 'link_preview', 'link_to_page', 'numbered_list_item',
    'paragraph', 'pdf', 'quote', 'synced_block', 'table', 'table_of_contents', 'table_row',
    'template', 'to_do', 'toggle', 'unsupported', 'video', 'code', 'mention'
]

color_enum = [
    'blue', 'blue_background', 'brown', 'brown_background', 'default', 'gray', 'gray_background',
    'green', 'green_background', 'orange', 'orange_background', 'yellow', 'yellow_background',
    'pink', 'pink_background', 'purple', 'purple_background', 'red', 'red_background'
]

rich_text_annotations_model = api.model('RichTextAnnotations', {
    'bold': fields.Boolean(description='Bold text'),
    'italic': fields.Boolean(description='Italic text'),
    'strikethrough': fields.Boolean(description='Strikethrough text'),
    'underline': fields.Boolean(description='Underline text'),
    'code': fields.Boolean(description='Code text'),
    'color': fields.String(description='Text color', enum=color_enum)
})

rich_text_model = api.model('RichText', {
    'type': fields.String(required=True, description='Type of the rich text object',
                          enum=['text', 'mention', 'equation']),
    'text': fields.Nested(api.model('RichTextText', {
        'content': fields.String(required=True, description='Content of the text'),
        'link': fields.String(description='URL of any link or Notion mention in this text, if any')
    })),
    'annotations': fields.Nested(rich_text_annotations_model, description='Annotations for styling the text'),
    'plain_text': fields.String(required=True, description='Plain text without annotations'),
    'href': fields.String(description='URL of any link or Notion mention in this text, if any')
})

mention_model = api.model('MentionBlock', {
    'type': fields.String(required=True, description='Type of the mention',
                          enum=['database', 'date', 'link_preview', 'page', 'user']),
    'database': fields.Nested(api.model('MentionDatabase', {
        'id': fields.String(required=True, description='ID of the database')
    }), required=False),
    'date': fields.Nested(api.model('MentionDate', {
        'start': fields.String(required=True, description='Start date'),
        'end': fields.String(description='End date'),
        'time_zone': fields.String(description='Time zone')
    }), required=False),
    'link_preview': fields.Nested(api.model('MentionLinkPreview', {
        'url': fields.String(required=True, description='URL of the link preview')
    }), required=False),
    'page': fields.Nested(api.model('MentionPage', {
        'id': fields.String(required=True, description='ID of the page')
    }), required=False),
    'user': fields.Nested(api.model('MentionUser', {
        'id': fields.String(required=True, description='ID of the user')
    }), required=False)
})

bulleted_list_item_model = api.model('BulletedListItemBlock', {
    'rich_text': fields.List(fields.Nested(rich_text_model), description='Rich text content of the bulleted list item'),
    'color': fields.String(description='Color of the block', enum=color_enum),
    'children': fields.List(fields.Nested(api.model('ChildBlock', {
        'type': fields.String(required=True, description='The type of the child block'),
        'text': fields.String(description='Text content of the child block')
    })), description='Children blocks')
})

callout_model = api.model('CalloutBlock', {
    'rich_text': fields.List(fields.Nested(rich_text_model), description='Rich text content of the callout'),
    'icon': fields.Nested(api.model('CalloutIcon', {
        'emoji': fields.String(description='Emoji for the callout icon')
    }), description='Icon of the callout'),
    'color': fields.String(description='Color of the block', enum=color_enum)
})

code_model = api.model('CodeBlock', {
    'caption': fields.List(fields.Nested(rich_text_model), description='Caption of the code block'),
    'rich_text': fields.List(fields.Nested(rich_text_model), description='Rich text content of the code block'),
    'language': fields.String(description='Language of the code', enum=[
        'abap', 'arduino', 'bash', 'basic', 'c', 'clojure', 'coffeescript', 'c++', 'c#', 'css', 'dart', 'diff',
        'docker',
        'elixir', 'elm', 'erlang', 'flow', 'fortran', 'f#', 'gherkin', 'glsl', 'go', 'graphql', 'groovy', 'haskell',
        'html', 'java', 'javascript', 'json', 'julia', 'kotlin', 'latex', 'less', 'lisp', 'livescript', 'lua',
        'makefile', 'markdown', 'markup', 'matlab', 'mermaid', 'nix', 'objective-c', 'ocaml', 'pascal', 'perl', 'php',
        'plain text', 'powershell', 'prolog', 'protobuf', 'python', 'r', 'reason', 'ruby', 'rust', 'sass', 'scala',
        'scheme', 'scss', 'shell', 'sql', 'swift', 'typescript', 'vb.net', 'verilog', 'vhdl', 'visual basic',
        'webassembly', 'xml', 'yaml', 'java/c/c++/c#'
    ])
})

heading_1_model = api.model('Heading1Block', {
    'rich_text': fields.List(fields.Nested(rich_text_model), description='Rich text content of the heading'),
    'color': fields.String(description='Color of the block', enum=color_enum),
    'is_toggleable': fields.Boolean(description='Is the heading toggleable')
})

heading_2_model = api.model('Heading2Block', {
    'rich_text': fields.List(fields.Nested(rich_text_model), description='Rich text content of the heading'),
    'color': fields.String(description='Color of the block', enum=color_enum),
    'is_toggleable': fields.Boolean(description='Is the heading toggleable')
})

heading_3_model = api.model('Heading3Block', {
    'rich_text': fields.List(fields.Nested(rich_text_model), description='Rich text content of the heading'),
    'color': fields.String(description='Color of the block', enum=color_enum),
    'is_toggleable': fields.Boolean(description='Is the heading toggleable')
})

link_preview_model = api.model('LinkPreviewBlock', {
    'url': fields.String(required=True, description='URL of the link preview')
})

image_model = api.model('ImageBlock', {
    'type': fields.String(required=True, description='Type of the image'),
    'external': fields.Nested(api.model('ImageExternal', {
        'url': fields.String(required=True, description='URL of the image')
    }), description='External image URL')
})

equation_model = api.model('EquationBlock', {
    'expression': fields.String(required=True, description='Expression of the equation')
})

embed_model = api.model('EmbedBlock', {
    'url': fields.String(required=True, description='URL of the embed')
})

divider_model = api.model('DividerBlock', {
})

column_model = api.model('ColumnBlock', {})

column_list_model = api.model('ColumnListBlock', {})

child_page_model = api.model('ChildPageBlock', {
    'title': fields.String(required=True, description='Title of the child page')
})

child_database_model = api.model('ChildDatabaseBlock', {
    'title': fields.String(required=True, description='Title of the child database')
})

breadcrumb_model = api.model('BreadcrumbBlock', {})

pdf_model = api.model('PDFBlock', {
    'type': fields.String(required=True, description='Type of the PDF'),
    'external': fields.Nested(api.model('PDFExternal', {
        'url': fields.String(required=True, description='URL of the PDF')
    }), description='External PDF URL')
})

numbered_list_item_model = api.model('NumberedListItemBlock', {
    'rich_text': fields.List(fields.Nested(rich_text_model), description='Rich text content of the numbered list item'),
    'color': fields.String(description='Color of the block', enum=color_enum),
    'children': fields.List(fields.Nested(api.model('ChildBlock', {
        'type': fields.String(required=True, description='The type of the child block'),
        'text': fields.String(description='Text content of the child block')
    })), description='Children blocks')
})

synced_block_model = api.model('SyncedBlock', {
    'synced_from': fields.Nested(api.model('SyncedFrom', {
        'block_id': fields.String(required=True, description='ID of the original synced block')
    }), required=False)
})

table_model = api.model('TableBlock', {
    'table_width': fields.Integer(required=True, description='Number of columns in the table'),
    'has_column_header': fields.Boolean(description='Whether the table has a column header'),
    'has_row_header': fields.Boolean(description='Whether the table has a row header')
})

table_row_model = api.model('TableRowBlock', {
    'cells': fields.List(fields.List(fields.Nested(rich_text_model)),
                         description='Cells content in horizontal display order')
})

video_model = api.model('VideoBlock', {
    'type': fields.String(required=True, description='Type of the video'),
    'external': fields.Nested(api.model('VideoExternal', {
        'url': fields.String(required=True, description='URL of the video')
    }), description='External video URL')
})

toggle_model = api.model('ToggleBlock', {
    'rich_text': fields.List(fields.Nested(rich_text_model), description='Rich text content of the toggle'),
    'color': fields.String(description='Color of the block', enum=color_enum),
    'children': fields.List(fields.Nested(api.model('ChildBlock', {
        'type': fields.String(required=True, description='The type of the child block'),
        'text': fields.String(description='Text content of the child block')
    })), description='Children blocks')
})

to_do_model = api.model('ToDoBlock', {
    'rich_text': fields.List(fields.Nested(rich_text_model), description='Rich text content of the ToDo'),
    'checked': fields.Boolean(description='Checked status for to_do blocks'),
    'color': fields.String(description='Color of the block', enum=color_enum),
    'children': fields.List(fields.Nested(api.model('ChildBlock', {
        'type': fields.String(required=True, description='The type of the child block'),
        'text': fields.String(description='Text content of the child block')
    })), description='Children blocks')
})

table_of_contents_model = api.model('TableOfContentsBlock', {
    'color': fields.String(description='Color of the block', enum=color_enum)
})

bookmark_model = api.model('BookmarkBlock', {
    'caption': fields.List(fields.Nested(rich_text_model), description='Caption of the bookmark'),
    'url': fields.String(required=True, description='URL of the bookmark')
})

paragraph_model = api.model('ParagraphBlock', {
    'rich_text': fields.List(fields.Nested(rich_text_model))
}, required=True, description='The rich text in the paragraph block')

block_content_model = api.model('BlockContent', {
    'type': fields.String(required=True, description='The type of the block', enum=block_type_enum),
    'embed': fields.Nested(embed_model, description='URL for embed blocks'),
    'children': fields.List(fields.Raw(), description='Children blocks'),
    'bookmark': fields.Nested(bookmark_model, description='Bookmark block specific content', required=False),
    'heading_1': fields.Nested(heading_1_model, description='Heading 1 block specific content', required=False),
    'heading_2': fields.Nested(heading_2_model, description='Heading 2 block specific content', required=False),
    'heading_3': fields.Nested(heading_3_model, description='Heading 3 block specific content', required=False),
    'link_preview': fields.Nested(link_preview_model, description='Link preview block specific content',
                                  required=False),
    'paragraph': fields.Nested(paragraph_model, description='Paragraph block specific content', required=False),
    'image': fields.Nested(image_model, description='Image block specific content', required=False),
    'equation': fields.Nested(equation_model, description='Equation block specific content', required=False),
    'divider': fields.Nested(divider_model, description='Divider block specific content', required=False),
    'column': fields.Nested(column_model, description='Column block specific content', required=False),
    'column_list': fields.Nested(column_list_model, description='Column list block specific content', required=False),
    'child_page': fields.Nested(child_page_model, description='Child page block specific content', required=False),
    'child_database': fields.Nested(child_database_model, description='Child database block specific content',
                                    required=False),
    'breadcrumb': fields.Nested(breadcrumb_model, description='Breadcrumb block specific content', required=False),
    'pdf': fields.Nested(pdf_model, description='PDF block specific content', required=False),
    'bulleted_list_item': fields.Nested(bulleted_list_item_model,
                                        description='Bulleted list item block specific content', required=False),
    'callout': fields.Nested(callout_model, description='Callout block specific content', required=False),
    'code': fields.Nested(code_model, description='Code block specific content', required=False),
    'numbered_list_item': fields.Nested(numbered_list_item_model,
                                        description='Numbered list item block specific content', required=False),
    'synced_block': fields.Nested(synced_block_model, description='Synced block specific content', required=False),
    'table': fields.Nested(table_model, description='Table block specific content', required=False),
    'table_row': fields.Nested(table_row_model, description='Table row block specific content', required=False),
    'video': fields.Nested(video_model, description='Video block specific content', required=False),
    'toggle': fields.Nested(toggle_model, description='Toggle block specific content', required=False),
    'to_do': fields.Nested(to_do_model, description='To do block specific content', required=False),
    'table_of_contents': fields.Nested(table_of_contents_model, description='Table of contents block specific content',
                                       required=False),
    'mention': fields.Nested(mention_model, description='Mention block specific content', required=False)
})

block_model = api.model('Block', {
    'object': fields.String(required=True, description='Always “block”.'),
    'id': fields.String(required=True, description='Identifier for the block'),
    'parent': fields.Raw(description='Information about the block`s parent'),
    'type': fields.String(required=True, description='Type of block', enum=block_type_enum),
    'created_time': fields.String(description='Date and time when this block was created'),
    'created_by': fields.Raw(description='User who created the block'),
    'last_edited_time': fields.String(description='Date and time when this block was last updated'),
    'last_edited_by': fields.Raw(description='User who last edited the block'),
    'archived': fields.Boolean(description='The archived status of the block'),
    'in_trash': fields.Boolean(description='Whether the block has been deleted'),
    'has_children': fields.Boolean(description='Whether or not the block has children blocks nested within it'),
    'block_type_data': fields.Nested(block_content_model,
                                     description='An object containing type-specific block information')
})

append_block_model = api.model('AppendBlockChildren', {
    'block_id': fields.String(required=True, description='The ID of the parent block'),
    'children': fields.List(fields.Nested(block_content_model), required=True,
                            description='List of children blocks to append')
})

update_block_model = api.model('UpdateBlock', {
    'id': fields.String(required=True, description='The ID of the block to update'),
    'block_type_data': fields.Nested(block_content_model,
                                     description='An object containing type-specific block information')
})

create_block_model = api.model('CreateBlock', {
    'page_id': fields.String(required=True, description='The ID of the page to add the block to'),
    'block_type_data': fields.List(
        fields.Nested(block_content_model, description='List of blocks to add'),
        description='List of blocks for creating')
})

api.models[create_block_model.name] = create_block_model
api.models[update_block_model.name] = update_block_model
api.models[append_block_model.name] = append_block_model
api.models[block_model.name] = block_model
api.models[embed_model.name] = embed_model
