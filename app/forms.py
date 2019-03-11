from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField
from wtforms import TextField
from wtforms import HiddenField 
from wtforms.validators import DataRequired


class ChannelForm(FlaskForm):
    channelId = TextField('ChannelId', validators=[DataRequired()])

class WebsiteForm(FlaskForm):
	base_url = StringField('Website Base Url', validators=[DataRequired()])
	rss_url = StringField('Rss_feed Url', validators=[DataRequired()])
	origin = StringField('Where did you find this?')

class RefreshForm(FlaskForm):
	update_video = BooleanField('Update Missing Video Stats', validators=[DataRequired()])

class VideoSearchForm(FlaskForm):
	search_query = BooleanField('Search for Video Title', validators=[DataRequired()])

class UpdateSiteForm(FlaskForm):
	rss_url = StringField('Rss_feed Url', validators=[DataRequired()])

class ConfirmTssForm(FlaskForm):
	confirm = BooleanField('This is a TTS', validators=[DataRequired()])
	channelID = HiddenField('CID', validators=[DataRequired()])
	notes = TextField('Notes')
	
	
class ProcessFilesForm(FlaskForm):
	begin = BooleanField('Begin processing articles', validators=[DataRequired()])
