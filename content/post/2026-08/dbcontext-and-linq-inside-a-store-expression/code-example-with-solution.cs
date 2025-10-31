public class UserCommentsQueryHandler: IRequestHandler <UserCommentsQuery, Paging<UserCommentResult>>
{
	private readonly UserService _userService;
	/// <summary>
	/// The two repositories have distinct context. 
	/// LINQ will not allow to perform the search with two DbContexts.
	/// </summary>
	private readonly DbContext _context;
	public UserCommentsQueryHandler(UserService userService, BookRespository bookRepository, VideoGameRespository videoGameRepository)
	{
		_userService = userService;
		// SOLUTION
		_context = _bookRepository.UnitOfWork.Context;
	}
	public Task <Paging<UserCommentResult>> Handle(UserCommentsQuery request, CancellationToken cancellationToken)
	{
		var currentUser = _userService.GetUserProfileDetails();
		var books = Extract<Book>(
			_context.Set<Book>(), 
			currentUser,
			(media, comment) => new UserCommentResult
			{
				Title = media.BeneficiaryAccount,
					Author = media.Author,
					Comment = comment.Id.ToString(),
					CommentedBy = comment.Name,
					CommentCreatedOn = comment.CreatedOn,
			});
		var videoGames = Extract<mediaInternal>(
			_context.Set<VideoGame>(), 
			currentUser,
			(media, comment) => new UserCommentResult
			{
				Title = media.BeneficiaryAccount,
					Author = media.Author,
					Comment = comment.Id.ToString(),
					CommentedBy = comment.Name,
			});
		var union = boooks.Union(videoGames);
		var search = PerformSearch(union, request.SearchText)
			.OrderByDescending(element => element.CommentCreatedOn);
		var result = search.Gridify(request.GridifyQuery);
		return Task.FromResult(result);
	}
}