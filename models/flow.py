from .odefunc import ODEfunc, ODEnet
from .normalization import MovingBatchNorm1d
from .ACNF import ACNF, SequentialFlow


def count_nfe(model):
    class AccNumEvals(object):

        def __init__(self):
            self.num_evals = 0

        def __call__(self, module):
            if isinstance(module, ACNF):
                self.num_evals += module.num_evals()

    accumulator = AccNumEvals()
    model.apply(accumulator)
    return accumulator.num_evals


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def count_total_time(model):
    class Accumulator(object):

        def __init__(self):
            self.total_time = 0

        def __call__(self, module):
            if isinstance(module, ACNF):
                self.total_time = self.total_time + module.sqrt_end_time * module.sqrt_end_time

    accumulator = Accumulator()
    model.apply(accumulator)
    return accumulator.total_time


def build_model(args, input_dim, hidden_dims, context_dim, num_blocks, conditional):
    def build_cnf():
        diffeq = ODEnet(
            hidden_dims=hidden_dims,
            input_shape=(input_dim,),
            context_dim=context_dim,
            layer_type=args.layer_type,
            nonlinearity=args.nonlinearity,
        )
        odefunc = ODEfunc(
            diffeq=diffeq,
        )
        cnf = ACNF(
            odefunc=odefunc,
            T=args.time_length,
            train_T=args.train_T,
            conditional=conditional,
            solver=args.solver,
            use_adjoint=args.use_adjoint,
            atol=args.atol,
            rtol=args.rtol,
        )
        return cnf
    chain = [build_cnf() for _ in range(num_blocks)]
    if args.batch_norm:
        bn_layers = [MovingBatchNorm1d(input_dim, bn_lag=args.bn_lag, sync=args.sync_bn)
                     for _ in range(num_blocks)]
        bn_chain = [MovingBatchNorm1d(input_dim, bn_lag=args.bn_lag, sync=args.sync_bn)]
        for a, b in zip(chain, bn_layers):
            bn_chain.append(a)
            bn_chain.append(b)
        chain = bn_chain
    model = SequentialFlow(chain)

    return model


def get_point_cnf(args):
    dims = tuple(map(int, args.dims.split("-")))
    model = build_model(args, args.input_dim, dims, args.zdim, args.num_blocks, True).cuda()
    print("Number of trainable parameters of Point CNF: {}".format(count_parameters(model)))
    return model


def get_latent_cnf(args):
    dims = tuple(map(int, args.latent_dims.split("-")))
    model = build_model(args, args.zdim, dims, 0, args.latent_num_blocks, False).cuda()
    print("Number of trainable parameters of Latent CNF: {}".format(count_parameters(model)))

    return model
