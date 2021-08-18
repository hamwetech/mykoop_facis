from django import forms
from activity.models import ThematicArea, TrainingSession, ExternalTrainer, TestItem, SoilTestSample, SoilTest
from conf.utils import bootstrapify



class ThematicAreaForm(forms.ModelForm):
    class Meta:
        model = ThematicArea
        fields = ['thematic_area', 'description']
        

class TrainingForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        exclude = ['create_date', 'update_date', 'created_by' , 'training_reference']
    
    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields['coop_member'].widget.attrs['id'] = 'selec_adv_1'
        

class ExternaTrainerForm(forms.ModelForm):
    class Meta:
        model = ExternalTrainer
        exclude = ['create_date', 'update_date']


class TestItemForm(forms.ModelForm):
    class Meta:
        model = TestItem
        exclude = ['create_date', 'update_date', 'created_by']


class SoilTestSampleForm(forms.ModelForm):
    class Meta:
        model = SoilTestSample
        exclude = ['create_date', 'update_date', 'created_by', 'soil_test']


class SoilTestForm(forms.ModelForm):
    class Meta:
        model = SoilTest
        exclude = ['create_date', 'update_date', 'created_by', 'recommendation']


bootstrapify(SoilTestForm)
bootstrapify(SoilTestSampleForm)
bootstrapify(TestItemForm)
bootstrapify(ExternaTrainerForm)
bootstrapify(ThematicAreaForm)
bootstrapify(TrainingForm)