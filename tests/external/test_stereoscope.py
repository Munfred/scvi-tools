import numpy as np

from scvi.data import synthetic_iid
from scvi.external import RNAStereoscope, SpatialStereoscope


def test_stereoscope(save_path):
    dataset = synthetic_iid(n_labels=5)

    # train with no proportions
    sc_model = RNAStereoscope(dataset)
    sc_model.train(max_epochs=1)

    # train again with proportions
    sc_model = RNAStereoscope(dataset, ct_weights=np.ones((5,)))
    sc_model.train(max_epochs=1)
    # test save/load
    sc_model.save(save_path, overwrite=True, save_anndata=True)
    sc_model = RNAStereoscope.load(save_path)

    st_model = SpatialStereoscope.from_rna_model(
        dataset, sc_model, prior_weight="minibatch"
    )
    st_model.train(max_epochs=1)
    st_model.get_proportions()
    # test save/load
    st_model.save(save_path, overwrite=True, save_anndata=True)
    st_model = SpatialStereoscope.load(save_path)
    st_model.get_proportions()

    # try imputation code
    ind_x = np.arange(50)[:, np.newaxis].astype(np.long)
    y = np.zeros((50, 1), np.long)
    st_model.get_scale_for_ct(ind_x, ind_x, y)
