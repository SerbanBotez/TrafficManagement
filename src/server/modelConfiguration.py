from omegaconf import OmegaConf

config = OmegaConf.load('config.yaml')


def configure_model(model):
    classes_dict = dict(config.MODEL.CLASSES)
    model.classes = list(classes_dict.values())
    # model.conf = 0.5
    # model.iou = 0.5
    # model.agnostic = False
    # model.multi_label = True

    return model
