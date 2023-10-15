agent_cfg = dict(
    type="PPO",
    gamma=0.95,
    lmbda=0.95,
    critic_coeff=0.5,
    entropy_coeff=0,
    critic_clip=False,
    obs_norm=False,
    rew_norm=True,
    adv_norm=True,
    recompute_value=True,
    num_epoch=2,
    critic_warmup_epoch=4,
    batch_size=1024,
    detach_actor_feature=False,
    max_grad_norm=0.5,
    eps_clip=0.2,
    max_kl=0.2,
    dual_clip=None,
    shared_backbone=False,
    ignore_dones=True,
    actor_cfg=dict(
        type="ContinuousActor",
        head_cfg=dict(
            type="GaussianHead",
            init_log_std=-1,
            clip_return=True,
            predict_std=False,
        ),
        nn_cfg=dict(
            type="LinearMLP",
            norm_cfg=None,
            mlp_spec=["obs_shape", 256, 256, "action_shape"],
            bias="auto",
            inactivated_output=True,
            # zero_init_output=True,
            linear_init_cfg=dict(
                type="xavier_init",
                gain=1,
                bias=0,
            ),
        ),
        optim_cfg=dict(type="Adam", lr=3e-4), 
        # For our PPO implementation, we need to prevent actor_optim from updating visual_nn as long as shared_backbone=True.
        # This is because we use (actor_loss + critic_loss).backward(), then apply actor_optim.step() and critic_optim.step() immediately afterwards.
        # Thus we need to prevent the visual backbone from being updated twice.
    ),
    critic_cfg=dict(
        type="ContinuousCritic",
        nn_cfg=dict(
            type="LinearMLP",
            norm_cfg=None,
            bias="auto",
            mlp_spec=["obs_shape", 256, 256, 1],
            inactivated_output=True,
            # zero_init_output=True,
            linear_init_cfg=dict(
                type="xavier_init",
                gain=1,
                bias=0,
            ),
        ),
        optim_cfg=dict(type="Adam", lr=3e-4),
    ),
)


train_cfg = dict(
    on_policy=True,
    total_steps=int(2e7),
    warm_steps=0,
    n_steps=int(2e4),
    n_updates=1,
    n_eval=int(2e5),
    n_checkpoint=int(2e5),
    ep_stats_cfg=dict(
        info_keys_mode=dict(
            success=[True, "max", "mean"],
        )
    ),
)


env_cfg = dict(
    type="gym",
    env_name="PickCube-v0",
    obs_mode='state',
    ignore_dones=True,
)


replay_cfg = dict(
    type="ReplayMemory",
    capacity=int(2e4),
)

rollout_cfg = dict(
    type="Rollout",
    num_procs=16,
    with_info=True,
    multi_thread=False,
)

eval_cfg = dict(
    type="Evaluation",
    num_procs=1,
    num=10,
    use_hidden_state=False,
    save_traj=False,
    save_video=True,
    log_every_step=False,
    env_cfg=dict(ignore_dones=False),
)