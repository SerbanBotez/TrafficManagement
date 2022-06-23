from omegaconf import OmegaConf

config = OmegaConf.load('config.yaml')


def configure_model(model):
    classes_dict = dict(config.MODEL.CLASSES)
    model.classes = list(classes_dict.values())

    return model
